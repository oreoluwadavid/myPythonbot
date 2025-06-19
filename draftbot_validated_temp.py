# draftbot_validated_temp.py
# Contains improved sections of draftbot.py with added input validation.
# Manually integrate these into your main draftbot.py file.

import pandas as pd
import numpy as np
import datetime
import math
import ast # For safe literal evaluation if extracts() is included
import os # For environment variable access in Portfolio

# It's assumed that other necessary classes like APImode, Message,
# various Indicator subclasses (MACD, ExponentialMovingAverage etc.) are defined
# in the main draftbot.py and will be in scope when these snippets are integrated.

# --- Utility Functions ---

def listsplit(list1: list, n: int):
    if not isinstance(list1, list):
        raise TypeError("Input 'list1' must be a list.")
    if not isinstance(n, int):
        raise TypeError("Input 'n' must be an integer.")
    # n can be negative or larger than list length, current logic handles this by returning empty or full list.
    list2 = []
    p = 0
    for item in list1:
        if p <= n: # Original logic kept, effectively means n is max_index + 1
            list2.append(item)
        else:
            break # More efficient than continue
        p += 1
    return list2

def list_to_str_float_list(lis1: list) -> list:
    if not isinstance(lis1, list):
        raise TypeError("Input 'lis1' must be a list.")
    lis2 = []
    for item_idx, items in enumerate(lis1): # Use enumerate for better error reporting if needed
        if isinstance(items, str):
            if items != "0" and items.endswith('4'): # Original condition items != 0 (as str)
                try:
                    parts = items.split('-')
                    if len(parts) > 2:
                        sub_parts = parts[2].split(' ')
                        if len(sub_parts) > 4:
                            val_part = sub_parts[4].split('N')
                            if len(val_part) > 0:
                                a = float(val_part[0])
                                lis2.append(a)
                            else:
                                print(f"Warning: list_to_str_float_list: Item '{items}' at index {item_idx} has 'N' but no value after it. Keeping original.")
                                lis2.append(items)
                        else:
                            print(f"Warning: list_to_str_float_list: Item '{items}' at index {item_idx} has insufficient space-separated parts. Keeping original.")
                            lis2.append(items)
                    else:
                        print(f"Warning: list_to_str_float_list: Item '{items}' at index {item_idx} has insufficient dash-separated parts. Keeping original.")
                        lis2.append(items)
                except ValueError:
                    print(f"Warning: list_to_str_float_list: Could not convert part of '{items}' to float. Keeping original.")
                    lis2.append(items)
                except IndexError:
                    print(f"Warning: list_to_str_float_list: String format of '{items}' is unexpected for parsing. Keeping original.")
                    lis2.append(items)
            else:
                lis2.append(items)
        elif isinstance(items, (int, float)):
            # Original behavior: if any item is already num, return original list immediately
            # This seems like a bug if the intent is to process all strings.
            # For now, preserving original behavior. If mixed list processing is desired, this should change.
            return lis1
        else:
            # If item is not str, int, or float, append as is or raise error.
            # Original code implicitly appends if not str (e.g. if it's a list or dict within lis1)
            # but then the float() conversion for numbers would fail.
            # Let's assume lis1 should contain strings or numbers.
            print(f"Warning: list_to_str_float_list: Item '{items}' at index {item_idx} is not a string or number. Keeping original.")
            lis2.append(items)
    return lis2

def extracts(df, largest, key) -> list:
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Input 'df' must be a pandas DataFrame.")
    if key not in df.columns:
        raise KeyError(f"Key '{key}' not found in DataFrame columns.")
    if not isinstance(largest, int):
        raise TypeError("'largest' must be an integer.")
    if largest < 0:
        raise ValueError("'largest' must be a non-negative integer.")

    lirt = []
    # Ensure 'largest' does not exceed DataFrame length to prevent iloc errors
    num_to_extract = min(largest, len(df))

    for i in range(num_to_extract):
        val_str = df[key].iloc[i]
        try:
            val = ast.literal_eval(val_str) # Safely evaluate string literals
            lirt.append(val)
        except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError) as e:
            print(f"Warning: extracts: Could not evaluate string '{val_str}' at index {i} for key '{key}'. Error: {e}. Appending as original string.")
            lirt.append(val_str)
    return lirt

def list_taker(n_idx, j_list: list, k_mode: str): # Renamed for clarity
    if not isinstance(j_list, list):
        raise TypeError("Input 'j_list' must be a list.")
    if k_mode not in ("output", "in"):
        raise ValueError("Input 'k_mode' must be 'output' or 'in'.")

    if k_mode == "output":
        try:
            # Original logic was a bit ambiguous with j[0][n] vs j[n]
            # Assuming if j_list[0] is a list/tuple, it's a list of lists scenario
            if j_list and (isinstance(j_list[0], (list, tuple))):
                if not isinstance(n_idx, int) or not (0 <= n_idx < len(j_list[0])):
                    raise IndexError(f"Index 'n_idx' ({n_idx}) out of bounds for inner list of length {len(j_list[0])}.")
                return j_list[0][n_idx]
            else: # Treat j_list as a flat list
                if not isinstance(n_idx, int) or not (0 <= n_idx < len(j_list)):
                    raise IndexError(f"Index 'n_idx' ({n_idx}) out of bounds for list of length {len(j_list)}.")
                return j_list[n_idx]
        except IndexError as e:
            # Fallback for the original's nested try-except structure if the above doesn't cover it.
            # This part of original logic suggests 'j' could be complex.
            # For safer code, the structure of 'j' should be more predictable.
            # Re-raising with more context.
            raise IndexError(f"Error accessing element in list_taker with n_idx={n_idx}, k_mode='output'. Original error: {e}")
        except TypeError as e: # E.g. if j_list[0] is not subscriptable
             raise TypeError(f"Type error in list_taker with n_idx={n_idx}, k_mode='output'. Original error: {e}")

    else:  # k_mode == "in"
        k_indices = []
        for i, item_in_j in enumerate(j_list):
            if item_in_j == n_idx: # n_idx here is the value to search for
                k_indices.append(i)
        return k_indices

def chunk_based_on_no(lst, chunk_no):
    if not isinstance(lst, list):
        raise TypeError("Input 'lst' must be a list.")
    if not isinstance(chunk_no, int) or chunk_no <= 0:
        raise ValueError("Input 'chunk_no' must be a positive integer.")

    if not lst:
        return iter([]) # Return an empty iterator for empty list

    n_items_per_chunk = math.ceil(len(lst) / chunk_no)
    if n_items_per_chunk == 0 :
        n_items_per_chunk = 1 # Avoid n=0 if lst is not empty but chunk_no is huge

    for x in range(0, len(lst), int(n_items_per_chunk)):
        each_chunk = lst[x : int(n_items_per_chunk) + x]
        if len(each_chunk) < n_items_per_chunk:
            each_chunk = each_chunk + [None for _ in range(int(n_items_per_chunk) - len(each_chunk))]
        yield each_chunk

# --- Timer Class ---

class Timer(object):
    def __init__(self, days, hours):
        if not (isinstance(days, (list, tuple)) and len(days) == 3 and
                all(isinstance(d, int) for d in days)):
            raise TypeError("Timer 'days' must be a list or tuple of 3 integers (year, month, day).")
        if not (isinstance(hours, (list, tuple)) and len(hours) == 3 and
                all(isinstance(h, int) for h in hours)):
            raise TypeError("Timer 'hours' must be a list or tuple of 3 integers (hour, minute, second).")

        try:
            self.day = datetime.date(days[0], days[1], days[2])
        except ValueError as e:
            raise ValueError(f"Invalid date components in 'days': {days}. Error: {e}")

        try:
            self.time = datetime.time(hours[0], hours[1], hours[2])
        except ValueError as e:
            raise ValueError(f"Invalid time components in 'hours': {hours}. Error: {e}")

        self.days_orig = list(days) # Store original if needed
        self.hours_orig = list(hours)
        # self.today is set in check_date, not in init

    # ... (other Timer methods like check_time, check_date, date_diff_accurate would be here) ...
    # For this exercise, only __init__ is reconstructed with validation.

# --- CashflowStatementBot Class ---

class CashflowStatementBot(object):
    def __init__(self, initial_capital, commision=0.0, price_bought=0.0, price_sold=0.0, data_amount=0.0):
        if not isinstance(initial_capital, (int, float)):
            raise TypeError("CashflowStatementBot 'initial_capital' must be a number.")
        if initial_capital < 0:
            raise ValueError("CashflowStatementBot 'initial_capital' cannot be negative.")
        self.initial_capital = float(initial_capital)

        if not isinstance(commision, (int, float)) or commision < 0:
            raise ValueError("CashflowStatementBot 'commision' must be a non-negative number.")
        self.commision = float(commision)

        if not isinstance(data_amount, (int, float)) or data_amount < 0:
            raise ValueError("CashflowStatementBot 'data_amount' must be a non-negative number.")
        self.data_amount = float(data_amount)

        if not isinstance(price_bought, (pd.Series, int, float)):
            raise TypeError("CashflowStatementBot 'price_bought' must be a pandas Series, int, or float.")
        self.price_bought = price_bought

        if not isinstance(price_sold, (pd.Series, int, float)):
            raise TypeError("CashflowStatementBot 'price_sold' must be a pandas Series, int, or float.")
        self.price_sold = price_sold

        if isinstance(price_bought, pd.Series) and isinstance(price_sold, pd.Series):
            if not price_bought.index.equals(price_sold.index): # Ensure this check is valid even if one Series is empty
                if not (price_bought.empty or price_sold.empty): # Only warn if both are non-empty
                     print("Warning: CashflowStatementBot: price_bought and price_sold Series have different indexes.")

        self.last_capital = []
        # self.data (DataFrame) is typically initialized in _calc_expense based on price_bought.index

    # ... (other CashflowStatementBot methods would be here) ...

# --- Indicator Base Class ---

class Indicator(object):
    def __init__(self, windows):
        if not isinstance(windows, (int, list)):
            raise TypeError("Indicator 'windows' must be an integer or a list of integers.")
        if isinstance(windows, int):
            if windows <= 0:
                raise ValueError("Indicator 'windows' (if integer) must be positive.")
        elif isinstance(windows, list):
            if not windows:
                raise ValueError("Indicator 'windows' list cannot be empty.")
            if not all(isinstance(w, int) and w > 0 for w in windows):
                raise ValueError("All elements in Indicator 'windows' list must be positive integers.")
        self.window = windows

    def _validate_input_data(self, _input_data_):
        if not isinstance(_input_data_, (pd.DataFrame, pd.Series)):
            raise TypeError("Input '_input_data_' to Indicator must be a pandas DataFrame or Series.")
        if _input_data_.empty:
            raise ValueError("Input DataFrame/Series '_input_data_' cannot be empty.")
        # Derived classes should call this and then add their specific column checks.

    def output_(self, _input_data_):
        self._validate_input_data(_input_data_) # Basic validation
        return self._input_calculation(_input_data_) # Call specific calculation

    def _input_calculation(self, _input_data_):
        # This method should be overridden by subclasses.
        raise NotImplementedError("Indicator subclasses must implement _input_calculation.")

# --- Specific Indicator Example (Momentum) ---

class Momentum(Indicator):
    def __init__(self, windows, Type: str = 'normal'):
        if not isinstance(windows, int):
            raise TypeError("Momentum 'windows' must be an integer for this implementation.")
        super().__init__(windows)

        if Type not in ('normal', 'subtract'):
            raise ValueError("Momentum 'Type' parameter must be 'normal' or 'subtract'.")
        self.Type = Type
        self.trend = None

    def _input_calculation(self, _input_data_):
        # _input_data_ already validated for type (DF/Series) and non-empty by base output_ method.

        input_series = None
        if isinstance(_input_data_, pd.DataFrame):
            if 'Close' not in _input_data_.columns:
                raise KeyError("Momentum input DataFrame requires a 'Close' column.")
            input_series = _input_data_['Close']
        elif isinstance(_input_data_, pd.Series):
            input_series = _input_data_

        if input_series is None: # Should not happen if _validate_input_data is thorough
            raise ValueError("Could not determine input series for Momentum.")


        if self.Type == 'subtract':
            moment_series = input_series - input_series.shift(self.window)
            if isinstance(_input_data_, pd.DataFrame):
                # Create a copy to avoid SettingWithCopyWarning if _input_data_ is a slice
                df_copy = _input_data_.copy()
                df_copy['moment'] = moment_series
                return df_copy # Return the DataFrame with 'moment' column added
            return moment_series # Return the moment Series if input was a Series

        elif self.Type == 'normal':
            if input_series.empty:
                 raise ValueError("Cannot calculate normal momentum on an empty series.")

            if (input_series <= 0).any():
                print("Warning: Momentum 'normal' type: Input series contains non-positive values. Log will produce NaN/Inf.")

            with np.errstate(divide='ignore', invalid='ignore'):
                returns = np.log(input_series)

            returns = returns.replace([np.inf, -np.inf], np.nan).dropna()

            if len(returns) < 2:
                print(f"Warning: Momentum 'normal': Not enough valid data points ({len(returns)}) for linear regression.")
                self.trend = 0.0
                return self.trend # Return the scalar trend value

            x = np.arange(len(returns))
            try:
                slope, _, rvalue, _, _ = linregress(x, returns)
            except ValueError as e_linreg:
                print(f"Warning: Momentum 'normal': Linear regression failed. Error: {e_linreg}")
                self.trend = 0.0
                return self.trend

            annualized = (1 + slope)**252
            self.trend = annualized * (rvalue**2)
            return self.trend # Return the scalar trend value

        # This part of the original code for Momentum._input_ was problematic:
        # return _input_["moment"]
        # It assumes 'moment' column exists in _input_ (only true for Type=='subtract' and DF input)
        # and would fail for Type=='normal' or if _input_ was Series for 'subtract'.
        # The corrected logic above returns the relevant result directly from each branch.
        # If a consistent return type (e.g. always a Series or always a DataFrame) is needed,
        # the 'normal' branch would need to return a Series of repeated trend value.
        # For now, 'subtract' returns Series/DF, 'normal' returns float.
        raise RuntimeError(f"Unexpected Momentum Type: {self.Type}")


# --- Selector Class ---
# Assuming Selector and APImode base classes are defined in the main draftbot.py
class Selector(object): # Placeholder if not available from main draftbot
    pass

class Portfolio(object): # Placeholder if not available
    pass

# --- Reconstructed __init__ methods with validation ---

def validated_selector_init(self, risk=0.05, profit=3.0, entry: list = None,
                            exits: list = None, window: list = None, exit_window: list = None):
    if not isinstance(risk, (int, float)):
        raise TypeError("Selector 'risk' must be a number (int or float).")
    if not (0.0 <= float(risk) <= 1.0): # Allow 0.0 and 1.0 for risk
        raise ValueError("Selector 'risk' must be between 0.0 and 1.0 (inclusive).")
    self.target_risk = float(risk)

    if not isinstance(profit, (int, float)):
        raise TypeError("Selector 'profit' (target_profit) must be a number (int or float).")
    if float(profit) <= 0: # Profit target should be positive
        raise ValueError("Selector 'profit' (target_profit) must be positive.")
    self.target_profit = float(profit)

    self.entry = entry if entry is not None else ["macd", "macd2", "TRMA"]
    if not isinstance(self.entry, list) or not all(isinstance(e, str) for e in self.entry):
        raise TypeError("Selector 'entry' must be a list of strings.")

    self.exit = exits if exits is not None else ["rsie"]
    if not isinstance(self.exit, list) or not all(isinstance(ex, str) for ex in self.exit):
        raise TypeError("Selector 'exits' must be a list of strings.")

    self.windows = window if window is not None else [12]
    if not isinstance(self.windows, list):
        raise TypeError("Selector 'windows' must be a list.")

    self.exit_windows = exit_window if exit_window is not None else [9]
    if not isinstance(self.exit_windows, list):
        raise TypeError("Selector 'exit_windows' must be a list.")

    self.stockname = ""
    self.held = False
    # self.entries (list of class objects) is populated in trading_rule method.

def validated_portfolio_init(self, mail, mailpass, # mail/mailpass are for Message, not directly used by Portfolio after refactor
                             n=100, commision=15, data=7, windows=None, broker="Phil",
                             no_of_shre=None, rules=Selector, # Default rules to actual Selector class
                             API=None, # Default API to None, should be APImode or subclass
                             maximum=0.2, capital: float = 1000.0,
                             APIKeys_env=None, APIname_env=None, # For clarity, pass env vars if needed
                             period: int = 7, no_of_transaction: int = 5,
                             rulest=None, time=12, start_date_list=None):

    # Env vars should ideally be handled before calling this, or this init becomes complex.
    # For this reconstruction, we'll assume they are passed if needed, or defaults are used.

    # Parameter Validations
    if not isinstance(n, int) or n <= 0:
        raise ValueError("Portfolio 'n' (for listsplit) must be a positive integer.")
    self.n = n

    if not isinstance(commision, (int, float)) or float(commision) < 0:
        raise ValueError("Portfolio 'commision' must be a non-negative number.")
    self.commision = float(commision)

    if not isinstance(data, (int, float)) or float(data) < 0:
        raise ValueError("Portfolio 'data' (cost) must be a non-negative number.")
    self.data = float(data)

    self.windows = windows
    if windows is not None and not isinstance(windows, list):
        raise TypeError("Portfolio 'windows' for indicators must be a list or None.")

    if not isinstance(broker, str) or not broker.strip():
        raise ValueError("Portfolio 'broker' must be a non-empty string.")
    self.broker = broker.strip()

    if no_of_shre is not None and (not isinstance(no_of_shre, (int, float)) or float(no_of_shre) < 0):
        raise ValueError("Portfolio 'no_of_shre' must be a non-negative number if provided.")
    self.amount_shares = no_of_shre

    if not callable(rules): # Check if 'rules' is a class type
        raise TypeError("Portfolio 'rules' must be a callable class (e.g., a Selector subclass).")
    self.rules_class = rules

    if not callable(API):
        raise TypeError("Portfolio 'API' must be a callable class (e.g., an APImode subclass).")
    self.api_class = API

    # API instantiation now relies on parameters passed to Portfolio's __init__
    # For simplicity, assume APIKeys_env and APIname_env are passed if needed by API class.
    # In a real scenario, these would be fetched from os.environ before this call or Portfolio handles it.
    try:
        self.api = self.api_class(broker=self.broker, apikeys=APIKeys_env, apiname=APIname_env)
    except Exception as e:
        raise RuntimeError(f"Failed to instantiate API class {self.api_class.__name__}. Error: {e}")


    if not isinstance(maximum, (int, float)) or not (0.0 <= float(maximum) <= 1.0):
        raise ValueError("Portfolio 'maximum' (loss percentage) must be a number between 0.0 and 1.0.")
    self.maximum_loss_pct = float(maximum)

    if not isinstance(capital, (int, float)) or float(capital) <= 0:
        raise ValueError("Portfolio 'capital' must be a positive number.")
    self.initial_capital = float(capital)

    if not isinstance(period, int) or period <= 0:
        raise ValueError("Portfolio 'period' (e.g. days for transaction check) must be a positive integer.")
    self.period = period

    if not isinstance(no_of_transaction, int) or no_of_transaction <= 0:
        raise ValueError("Portfolio 'no_of_transaction' (max concurrent trades) must be a positive integer.")
    self.stockno = no_of_transaction

    self.rulest = rulest if rulest is not None else []
    if not isinstance(self.rulest, list):
        raise TypeError("Portfolio 'rulest' must be a list if provided.")

    if not isinstance(time, int) or not (0 <= time <= 23):
        raise ValueError("Portfolio 'time' (execution hour) must be an integer between 0 and 23.")
    self.settime = time

    effective_start_date_list = start_date_list if start_date_list is not None else [2019, 1, 1]
    if not (isinstance(effective_start_date_list, (list, tuple)) and len(effective_start_date_list) == 3 and
            all(isinstance(d_item, int) for d_item in effective_start_date_list)):
        raise TypeError("Portfolio 'start_date_list' must be a list or tuple of 3 integers (year, month, day).")
    try:
        self.startdate = datetime.datetime(effective_start_date_list[0], effective_start_date_list[1], effective_start_date_list[2])
    except ValueError as e:
        raise ValueError(f"Invalid date components in 'start_date_list': {effective_start_date_list}. Error: {e}")
    if start_date_list is None:
            print(f"Warning: Portfolio 'start_date_list' was not provided, defaulted to {self.startdate.strftime('%Y-%m-%d')}.")

    # Original attributes
    self.Bot = CashflowStatementBot
    self.transactions = pd.DataFrame()
    self.quit = False
    self.portofolio = []
    self.connected = False

    # Message class instantiation - assuming mail and mailpass are for this
    # If Message class loads from env, these params might not be needed here.
    # For this reconstruction, we pass them.
    if not (isinstance(mail, str) and isinstance(mailpass, str)): # Basic check
        raise TypeError("Portfolio: 'mail' and 'mailpass' for Message must be strings.")
    # self.ssage = Message(selfmail=mail, selfpass=mailpass) # Original name was self.ssage
    # Re-evaluating based on "Secure Email Transmission" that Message loads from env.
    # So mail, mailpass to Portfolio init are not for Message obj anymore.
    # self.ssage = Message() # If Message loads from env in its __init__

    self.maximumloss = self.maximum_loss_pct * self.initial_capital


# Example of how one might replace __init__ in the main file:
# setattr(Selector, '__init__', validated_selector_init)
# setattr(Portfolio, '__init__', validated_portfolio_init)

# Or, more directly, these functions would replace the content of the
# __init__ methods in the original draftbot.py file.
```
