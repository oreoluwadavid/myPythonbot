# draftbot_integrity_temp.py
# Contains helper functions for data integrity (SHA256 hashing)
# and examples of how to integrate them into Portfolio file I/O.
# Manually integrate these into your main draftbot.py file.

import hashlib
import io
import os
import pandas as pd # For context if Portfolio snippets use pd

# --- Hashing Helper Functions ---

def calculate_sha256(filepath):
    """Calculates the SHA256 hash of a file."""
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        print(f"Warning: calculate_sha256: File not found at {filepath}. Cannot calculate hash.")
        return None
    except Exception as e:
        print(f"Error calculating SHA256 for {filepath}: {e}")
        return None

def write_hash_file(data_filepath, hash_value):
    """Writes the hash value to a .sha256 file."""
    hash_filepath = data_filepath + ".sha256"
    try:
        with open(hash_filepath, "w") as hf:
            hf.write(hash_value)
    except Exception as e:
        print(f"Error writing hash file {hash_filepath}: {e}")

def read_hash_file(data_filepath):
    """Reads the hash value from a .sha256 file."""
    hash_filepath = data_filepath + ".sha256"
    try:
        with open(hash_filepath, "r") as hf:
            return hf.read().strip()
    except FileNotFoundError:
        # This is expected if the file is new or hash was never created
        return None
    except Exception as e:
        print(f"Error reading hash file {hash_filepath}: {e}")
        return None

def verify_file_integrity(filepath_to_check):
    """Verifies the integrity of a file against its stored hash."""
    print(f"Integrity: Verifying integrity of {filepath_to_check}...")
    expected_hash = read_hash_file(filepath_to_check)

    if not os.path.exists(filepath_to_check):
        if expected_hash is not None:
            # Hash file exists, but data file doesn't. This is an anomaly.
            raise ValueError(f"Integrity Check Failed: Data file {filepath_to_check} is missing, "
                             f"but its hash file exists. Possible tampering or deletion.")
        else:
            # Neither data file nor hash file exists. Treat as 'file not found', not an integrity error here.
            # The caller (e.g. Portfolio._main*) will handle FileNotFoundError for the data file.
            print(f"Integrity: Data file {filepath_to_check} and its hash file not found. Skipping integrity check.")
            return True # Or specific code indicating file not found for caller to handle

    if expected_hash is None:
        print(f"Warning: Integrity Check: Hash file for {filepath_to_check} not found. "
              f"Cannot verify integrity. Assuming valid if file exists, or create initial hash.")
        # Optionally, calculate and store hash for the first time if file exists but hash doesn't
        current_hash_for_new_file = calculate_sha256(filepath_to_check)
        if current_hash_for_new_file:
            print(f"Integrity: Creating initial hash for {filepath_to_check}.")
            write_hash_file(filepath_to_check, current_hash_for_new_file)
        return True # Cannot verify, but proceed

    current_hash = calculate_sha256(filepath_to_check)
    if current_hash is None: # Error during hash calculation for the data file
        raise ValueError(f"Integrity Check Failed: Could not calculate hash for {filepath_to_check}.")

    if current_hash != expected_hash:
        raise ValueError(f"Integrity Check Failed: Hash mismatch for {filepath_to_check}. "
                         f"File may be corrupted or tampered with. "
                         f"Expected: {expected_hash}, Got: {current_hash}")

    print(f"Integrity: File {filepath_to_check} verified successfully.")
    return True

def create_and_store_hash(filepath_to_hash):
    """Calculates and stores the hash for a file."""
    print(f"Integrity: Calculating and storing hash for {filepath_to_hash}...")
    current_hash = calculate_sha256(filepath_to_hash)
    if current_hash:
        write_hash_file(filepath_to_hash, current_hash)
        print(f"Integrity: Hash stored for {filepath_to_hash}.")
    else:
        print(f"Warning: Integrity: Could not calculate or store hash for {filepath_to_hash}.")


# --- Example Snippets for Portfolio._main* Methods ---
# You will need to adapt these snippets into your existing Portfolio class methods.
# Ensure `self.data_directory` is defined in your Portfolio class.

class PortfolioSnippets: # Wrapper class just for organizing these snippets

    # Example: Modifying part of Portfolio._main1 (or _main, _main2)
    # where CSV files are read and written.

    def example_portfolio_file_io_initialization(self):
        # This is a conceptual representation. `self.data_directory` must be set.
        # self.data_directory = os.getenv('PORTFOLIO_DATA_DIRECTORY') (should be in Portfolio.__init__)

        # These would be attributes of the Portfolio class, set in __init__ or early in the method
        # For example:
        # self.save_file_path = os.path.join(self.data_directory, "hist.txt")
        # self.time_file_path = os.path.join(self.data_directory, "time_file.csv")
        # self.dat_save_path = os.path.join(self.data_directory, "dat_save.csv")
        # self.price_values_path = os.path.join(self.data_directory, "price_values.csv")

        # Placeholder for actual file paths
        save_file_path = "path_to_hist.txt"
        time_file_path = "path_to_time_file.csv"
        dat_save_path = "path_to_dat_save.csv"
        price_values_path = "path_to_price_values.csv"


        try:
            # --- Reading files with integrity check ---
            # hist.txt (save_file) - special handling as it's just checked for existence mostly
            if os.path.exists(save_file_path):
                verify_file_integrity(save_file_path)
            else:
                # Create hist.txt and its hash if it's meant to be created here
                # with open(save_file_path, "w") as f:
                #     f.write("Initialization history marker.\n")
                # create_and_store_hash(save_file_path)
                # print(f"Integrity: Initialized {save_file_path} and its hash.")
                pass # Original logic for hist.txt creation would go here if applicable

            # time_file.csv
            # If verify_file_integrity returns False or raises an error, it needs to be handled.
            # The current verify_file_integrity raises ValueError on mismatch or returns True.
            verify_file_integrity(time_file_path) # Will raise error on mismatch or if hash calc fails
            time_file_df = pd.read_csv(time_file_path) # Proceed if no error
            # Store current values from time_file_df...

            # dat_save.csv
            verify_file_integrity(dat_save_path)
            dat_save_df = pd.read_csv(dat_save_path)
            # Store current values from dat_save_df...

            # price_values.csv
            verify_file_integrity(price_values_path)
            price_values_df = pd.read_csv(price_values_path)
            # Store current values from price_values_df...

            print("Integrity: All initial files loaded and verified successfully (if they existed and hashes matched).")

        except FileNotFoundError as e:
            # This block is for when the *data file itself* is not found by pd.read_csv,
            # and verify_file_integrity might have passed (e.g. hash also not found, treated as first run for that file).
            print(f"Info: Initial file load: A data file was not found by pandas: {e}. Proceeding with initialization logic.")
            # Standard initialization logic from original _main* method would follow here,
            # creating DataFrames and then saving them with hashes.

            # Example: if time_file_df was not loaded, initialize it
            # time_file_df = pd.DataFrame(...)
            # time_file_df.to_csv(time_file_path, index=False)
            # create_and_store_hash(time_file_path)

            # Similar for dat_save_df, price_values_df...
            pass # Fall through to original initialization logic

        except ValueError as e: # Catch integrity errors from verify_file_integrity
            print(f"CRITICAL: File integrity validation failed: {e}. Cannot proceed safely.")
            # Handle critical error: maybe halt operations, alert user, etc.
            raise # Re-raise or handle appropriately

        # ... rest of the initialization part of _main* method ...
        return # Example

    def example_portfolio_file_io_saving_at_end_of_day(self, time_file_df_instance, price_values_df_instance):
        # Conceptual representation of saving files at the end of a processing day/cycle
        # self.data_directory must be set.

        time_file_path = "path_to_time_file.csv" # os.path.join(self.data_directory, "time_file.csv")
        price_values_path = "path_to_price_values.csv" # os.path.join(self.data_directory, "price_values.csv")

        # Assume time_file_df_instance and price_values_df_instance are populated DataFrames
        # Example:
        # time_file_df_instance = pd.DataFrame(...)
        # price_values_df_instance = pd.DataFrame(...)

        try:
            time_file_df_instance.to_csv(time_file_path, index=False)
            create_and_store_hash(time_file_path)

            price_values_df_instance.to_csv(price_values_path, index=False)
            create_and_store_hash(price_values_path)

            print("Integrity: Daily data files saved and hashes updated.")
        except Exception as e:
            print(f"Error during daily data saving or hashing: {e}")
            # Handle error (e.g. log, alert)

    def example_portfolio_weekly_report_saving(self, ep_df, day_identifier_str):
        # Conceptual representation for saving weekly report
        # self.data_directory must be set.

        ep_filename = f"ep_day{day_identifier_str}.csv"
        ep_filepath = "path_to_weekly_report/" + ep_filename # os.path.join(self.data_directory, ep_filename)

        try:
            ep_df.to_csv(ep_filepath, index=False)
            create_and_store_hash(ep_filepath)
            print(f"Integrity: Weekly report {ep_filepath} saved and hash stored.")

            # Example: If this report is also an email attachment
            # message_instance = Message() # Assuming Message class is available and configured
            # message_instance.create_message("Weekly report attached.")
            # message_instance.send_message(attachment=ep_filepath)

        except Exception as e:
            print(f"Error saving or hashing weekly report {ep_filepath}: {e}")


# --- Instructions for Manual Integration ---
# 1. Add the helper functions `calculate_sha256`, `write_hash_file`,
#    `read_hash_file`, `verify_file_integrity`, and `create_and_store_hash`
#    to your main `draftbot.py` script, typically near the top with other utilities.
# 2. Ensure `import hashlib`, `import io`, `import os` are at the top of `draftbot.py`.
# 3. In your `Portfolio` class, within methods like `_main`, `_main1`, `_main2`:
#    a. Before reading a critical CSV file (e.g., `pd.read_csv(price_values_path)`),
#       call `verify_file_integrity(price_values_path)`. You must handle the
#       possibility of this function raising a `ValueError` if integrity check fails.
#       If `verify_file_integrity` returns `True` (or doesn't raise an error), proceed.
#    b. After writing a critical CSV file (e.g., `price_values_df.to_csv(price_values_path)`),
#       call `create_and_store_hash(price_values_path)`.
# 4. Adapt the example snippets above (`example_portfolio_file_io_initialization`, etc.)
#    to fit the specific logic and file names used in your `Portfolio` methods.
#    The snippets show conceptual placement; your actual code structure will dictate
#    precise integration. The placeholder paths like "path_to_time_file.csv" should be
#    replaced with actual path construction using `os.path.join(self.data_directory, filename)`.
# 5. Pay attention to `FileNotFoundError` during initial setup. `verify_file_integrity`
#    has logic to handle cases where hash files don't exist yet (e.g., first run)
#    and can create initial hashes if the data file exists.
# 6. Decide on a firm error handling strategy if `verify_file_integrity` raises a
#    `ValueError` (hash mismatch). The script might need to terminate or enter a
#    safe mode.

```
