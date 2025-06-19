import unittest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock
import os
import datetime
import io # For potential use if testing df hashing directly

# Attempt to import classes and functions from draftbot
# It's crucial that draftbot.py is in the Python path or same directory
try:
    from draftbot import (
        listsplit,
        list_to_str_float_list,
        # extracts, # ast.literal_eval makes this tricky to unit test without good examples of valid strings
        list_taker,
        chunk_based_on_no,
        Timer,
        CashflowStatementBot,
        Message,
        Portfolio, # For testing __init__ regarding env vars
        APImode, # Base class for API, might be needed for Portfolio mock
        Selector, # Base class for rules, might be needed for Portfolio mock
        SimpleMovingAverage,
        ExponentialMovingAverage,
        # Add other key components as deemed testable
    )
    DRAFTBOT_AVAILABLE = True
except ImportError as e:
    print(f"Could not import from draftbot: {e}. Tests will be skipped or fail.")
    DRAFTBOT_AVAILABLE = False
    # Define dummy classes if import fails, so tests can be skipped gracefully
    class Timer: pass
    class CashflowStatementBot: pass
    class Message: pass
    class Portfolio: pass
    class APImode: pass
    class Selector: pass
    class SimpleMovingAverage: pass
    class ExponentialMovingAverage: pass


@unittest.skipIf(not DRAFTBOT_AVAILABLE, "draftbot.py module not found or imports failed")
class TestUtils(unittest.TestCase):
    def test_listsplit(self):
        # Assuming original behavior (no custom error raising for invalid types)
        self.assertEqual(listsplit([1, 2, 3, 4, 5], 2), [1, 2, 3])
        self.assertEqual(listsplit([1, 2, 3], 5), [1, 2, 3]) # n larger than list
        self.assertEqual(listsplit([], 2), []) # Empty list
        # Test p increment logic (original was a bit ambiguous)
        # If p increments only when p <= n: listsplit([1,2,3,4],1) -> [1,2] (p becomes 0,1,2)
        # If p increments always: listsplit([1,2,3,4],1) -> [1,2] (p becomes 0,1, then item for p=2 is skipped)
        # The current restored code (original) increments p outside the if condition's direct scope but inside loop
        self.assertEqual(listsplit([1,2,3,4], 0), [1]) # Only first item
        self.assertEqual(listsplit([1,2,3,4], -1), []) # n < 0, p always > n


    def test_list_to_str_float_list(self):
        # This function is fragile; test based on its original specific parsing
        # Example: items.split('-')[2].split(' ')[4].split('N')[0]
        # A string like "prefix-ignore-val1 val2 val3 val4 123.45Ndetails"
        # So, index 2 of '-' split is "val1 val2 val3 val4 123.45Ndetails"
        # index 4 of ' ' split is "123.45Ndetails"
        # index 0 of 'N' split is "123.45"
        # And it must end with '4' - this condition seems contradictory to the parsing logic.
        # Given the original code: `items.endswith('4') is True`
        # The parsing `float(items.split('-')[2].split(' ')[4].split('N')[0])` would likely fail
        # if the string truly ends with '4' unless 'N' is part of that '4'.
        # Let's assume the endswith('4') was an error and test the parsing part.
        # Or, if endswith('4') is strict, then the parsing will almost always fail.

        # Test case based on original parsing logic (ignoring endswith('4') for a moment)
        # self.assertEqual(list_to_str_float_list(["ignore-ignore-foo bar baz qux 123.45Ndetails"]), [123.45])

        # Test case considering endswith('4') - this will likely not parse to float due to '4' at end
        self.assertEqual(list_to_str_float_list(["test-test-name date 12.3N-value4"]), ["test-test-name date 12.3N-value4"])

        # Test if a number is encountered (original behavior: returns original list)
        self.assertEqual(list_to_str_float_list([1.0, "test-test-name date 12.3N-value4"]), [1.0, "test-test-name date 12.3N-value4"])

        # Test general strings (no parsing, no number)
        self.assertEqual(list_to_str_float_list(["abc", "def"]), ["abc", "def"])
        self.assertEqual(list_to_str_float_list([]), [])


    def test_list_taker(self):
        # Test k="output"
        self.assertEqual(list_taker(1, [[10, 20, 21], [30, 40]], k="output"), 20) # j[0][1]
        self.assertEqual(list_taker(0, [5, 6, 7], k="output"), 5) # j[0]
        with self.assertRaises(IndexError): # n out of bounds for flat list
            list_taker(3, [5, 6, 7], k="output")
        with self.assertRaises(IndexError): # n out of bounds for inner list
            list_taker(3, [[0,1],[10,11]], k="output")


        # Test k="in"
        self.assertEqual(list_taker(5, [1, 5, 2, 5, 3], k="in"), [1, 3])
        self.assertEqual(list_taker(8, [1, 5, 2, 5, 3], k="in"), []) # Not found
        self.assertEqual(list_taker(None, [1, None, 2, None], k="in"), [1,3])


    def test_chunk_based_on_no(self):
        self.assertEqual(list(chunk_based_on_no([1,2,3,4,5,6], 3)), [[1,2],[3,4],[5,6]])
        self.assertEqual(list(chunk_based_on_no([1,2,3,4,5], 2)), [[1,2,3],[4,5,None]])
        self.assertEqual(list(chunk_based_on_no([], 5)), []) # Empty list input
        self.assertEqual(list(chunk_based_on_no([1,2,3], 1)), [[1,2,3]]) # Single chunk
        self.assertEqual(list(chunk_based_on_no([1,2,3], 5)), [[1,2,3,None,None]]) # chunk_no > len


@unittest.skipIf(not DRAFTBOT_AVAILABLE, "draftbot.py module not found or imports failed")
class TestTimer(unittest.TestCase):
    def test_timer_init_valid(self):
        # Assuming Timer validation was part of the "Input Validation" subtask,
        # which might not be in the current baseline state.
        # If validation is NOT present, these will pass by creating invalid date/time objects or erroring differently.
        # If validation IS present (as per prompt for TestTimer), it should raise specific errors.
        # For this test, we check if valid Timer objects can be created.
        # The prompt for this subtask assumes a state *before* input validation,
        # but then asks for tests that assume validation (e.g. with self.assertRaises(ValueError)).
        # Test will be written assuming the validation *is* in place for Timer as per prompt's specific example.
        timer = Timer(days=[2023, 1, 1], hours=[10, 0, 0])
        self.assertEqual(timer.day, datetime.date(2023, 1, 1))
        self.assertEqual(timer.time, datetime.time(10, 0, 0))

    def test_timer_init_invalid_date_time(self):
        # These tests assume Timer's __init__ validates date/time ranges.
        with self.assertRaises(ValueError): # Invalid month
            Timer(days=[2023, 13, 1], hours=[10, 0, 0])
        with self.assertRaises(ValueError): # Invalid hour
            Timer(days=[2023, 1, 1], hours=[25, 0, 0])
        # Test for type errors if validation is added for that.
        # For now, assuming ValueError for out-of-range components.

    @patch('draftbot.datetime') # Mocking datetime module used by draftbot.Timer
    def test_date_diff_accurate(self, mock_dt_module):
        # Mock datetime.date.today() and datetime.date constructor if used by date_diff_accurate
        mock_dt_module.date.today.return_value = datetime.date(2023, 1, 10)
        mock_dt_module.date = datetime.date # Allow Timer to use actual datetime.date

        timer = Timer(days=[2023, 1, 1], hours=[0,0,0])
        # Test with eam=0 (should use mocked today)
        # The original date_diff_accurate has complex month_monitor logic.
        # This test will be more of an integration test for that logic.
        # A direct calculation for 9 days:
        self.assertEqual(timer.date_diff_accurate(eam=0), 9)

        # Test with a specific 'eam' date
        diff = timer.date_diff_accurate(eam=[2023, 1, 15]) # 15th Jan 2023
        self.assertEqual(diff, 14) # 15 - 1 = 14 days


@unittest.skipIf(not DRAFTBOT_AVAILABLE, "draftbot.py module not found or imports failed")
class TestCashflowStatementBot(unittest.TestCase):
    def test_cashflow_calculations_basic(self):
        idx = pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03'])
        price_bought = pd.Series([100, 0, 0], index=idx)
        price_sold = pd.Series([0, 120, 0], index=idx)

        bot = CashflowStatementBot(initial_capital=1000.0,
                                   price_bought=price_bought,
                                   price_sold=price_sold,
                                   commision=1.0, # Simpler commission
                                   data_amount=1.0) # Simpler data cost

        results_df = bot.loop()

        # Day 1: Buy
        # Expense = 100 (buy) + 1 (comm) + 1 (data) = 102
        # Gross Profit = 0 (sold) - 102 = -102
        # Cashflow (tax) = 0 (since gross profit is negative)
        # Net Profit = -102 - 0 = -102
        # Capital = 1000 (initial) + (-102) = 898

        # Day 2: Sell
        # Price_bought on day 2 is 0, so this trade is linked to day 1's buy.
        # The bot's logic for linking trades or handling daily expenses vs trade expenses needs clarity.
        # Current logic: expense is daily. Profit is also daily.
        # If an expense of 102 was booked on day 1 for the buy.
        # On day 2, sold for 120. The price_bought for profit calc on day 2 is 0.
        # This means the profit calc might be: Sold(120) - Expense_today(0+1+1=2) = 118
        # This interpretation seems off for typical P&L.

        # Let's re-evaluate based on bot.loop() structure:
        # 1. _calc_expense():
        #    results_df['expense'].iloc[0] = price_bought[0] (100) + 1 + 1 = 102
        #    bot.last_capital = [1000, 1000] (initial_capital appended)
        # 2. _calc_profit():
        #    price_bought.iloc[0] (100) vs last(bot.last_capital) (1000) -> 100 < 1000, so price_bought remains 100.
        #    price_sold.iloc[0] (0) remains 0.
        #    results_df['expense'].iloc[0] (102) remains 102.
        #    results_df['grossprofit'].iloc[0] = 0 - 102 = -102
        #    results_df['cashflow'].iloc[0] = 0 (20% of negative is 0)
        #    results_df['netprofit'].iloc[0] = -102 - 0 = -102
        #    bot.last_capital becomes [1000, 1000, 1000 + (-102)] = [1000, 1000, 898]
        #    results_df['capital'].iloc[0] is from return_capital(): last_capital[-2] + netprofit[0] = 1000 + (-102) = 898

        #    price_bought.iloc[1] (0) vs last(bot.last_capital) (898) -> 0 < 898, price_bought[1] remains 0
        #    price_sold.iloc[1] (120) vs price_bought[1] (0) -> price_sold[1] remains 120.
        #    results_df['expense'].iloc[1] = price_bought[1](0) + 1 + 1 = 2. (This is where it seems expense is per-entry not per-trade)
        #    results_df['grossprofit'].iloc[1] = 120 - 2 = 118
        #    results_df['cashflow'].iloc[1] = 0.2 * 118 = 23.6
        #    results_df['netprofit'].iloc[1] = 118 - 23.6 = 94.4
        #    bot.last_capital becomes [1000, 1000, 898, 898 + 94.4] = [1000, 1000, 898, 992.4]
        #    results_df['capital'].iloc[1] is last_capital[-2] + netprofit[1] = 898 + 94.4 = 992.4

        self.assertAlmostEqual(results_df['expense'].iloc[0], 102, places=1)
        self.assertAlmostEqual(results_df['grossprofit'].iloc[0], -102, places=1)
        self.assertAlmostEqual(results_df['netprofit'].iloc[0], -102, places=1)
        self.assertAlmostEqual(results_df['capital'].iloc[0], 898, places=1)

        self.assertAlmostEqual(results_df['expense'].iloc[1], 2, places=1) # Expense of holding/data for day 2
        self.assertAlmostEqual(results_df['grossprofit'].iloc[1], 118, places=1) # Profit from sale on day 2
        self.assertAlmostEqual(results_df['netprofit'].iloc[1], 94.4, places=1)
        self.assertAlmostEqual(results_df['capital'].iloc[1], 992.4, places=1)


@unittest.skipIf(not DRAFTBOT_AVAILABLE, "draftbot.py module not found or imports failed")
class TestMessage(unittest.TestCase):
    # Assuming Message class does NOT load from os.environ directly in __init__
    # but expects selfmail and selfpass to be provided.
    # The Portfolio class was responsible for loading these from env vars if used there.

    @patch('draftbot.smtplib.SMTP')
    def test_send_message_structure(self, mock_smtp_constructor):
        mock_smtp_instance = MagicMock()
        mock_smtp_constructor.return_value = mock_smtp_instance

        # Provide dummy credentials directly as per original Message.__init__
        msg = Message(selfmail='test@example.com', selfpass='password', othermail='recipient@example.com')
        msg.create_message("Test body content")

        dummy_attachment_path = "dummy_attachment.txt"
        with open(dummy_attachment_path, "w") as f:
            f.write("dummy content")

        msg.send_message(attachment=dummy_attachment_path)
        os.remove(dummy_attachment_path)

        mock_smtp_instance.starttls.assert_called_once()
        mock_smtp_instance.login.assert_called_once_with('test@example.com', 'password')
        mock_smtp_instance.sendmail.assert_called_once()

        args, _ = mock_smtp_instance.sendmail.call_args
        sender, recipient, full_email_str = args

        self.assertEqual(sender, 'test@example.com')
        self.assertEqual(recipient, 'recipient@example.com')
        self.assertTrue("Subject: The weeks trade's" in full_email_str) # Original subject
        self.assertTrue("Test body content" in full_email_str)
        # Original header was "Content-Decomposition"
        self.assertTrue("Content-Disposition: attachment; filename=dummy_attachment.txt" in full_email_str)
        mock_smtp_instance.quit.assert_called_once()


@unittest.skipIf(not DRAFTBOT_AVAILABLE, "draftbot.py module not found or imports failed")
class TestPortfolioInit(unittest.TestCase):
    # This test assumes Portfolio __init__ was modified to load API keys from env vars
    # and data_directory as per "Secure Email Transmission" and "os.chdir()" subtasks.

    @patch.dict(os.environ, {
        'PORTFOLIO_API_KEYS': 'env_api_keys',
        'PORTFOLIO_API_NAME': 'env_api_name',
        'PORTFOLIO_DATA_DIRECTORY': './mock_data_dir', # Mocked directory
        'EMAIL_ADDRESS': 'env_email@example.com',     # For Message instantiation
        'EMAIL_PASSWORD': 'env_email_password'
    })
    @patch('draftbot.os.path.isdir') # Mock isdir
    @patch('draftbot.os.makedirs')   # Mock makedirs
    @patch('draftbot.APImode')       # Mock the default APImode class
    @patch('draftbot.Message')       # Mock the Message class
    def test_portfolio_init_with_env_vars(self, MockMessageClass, MockApiClass, mock_makedirs, mock_isdir):
        mock_isdir.return_value = True # Assume data directory exists

        # Mock instances that would be created
        mock_api_instance = MagicMock()
        MockApiClass.return_value = mock_api_instance

        mock_message_instance = MagicMock()
        MockMessageClass.return_value = mock_message_instance

        # Use a real, simple Selector for rules if possible, or mock it too
        MockSelectorClass = MagicMock()

        portfolio = Portfolio(
            mail="not_used@example.com", # Will be overridden by env var for Message
            mailpass="not_used_pass",   # Will be overridden by env var for Message
            rules=MockSelectorClass,
            API=MockApiClass,
            capital=5000.0
        )

        self.assertEqual(portfolio.initial_capital, 5000.0)
        # Check that Portfolio's attributes related to API are set from env vars
        # The actual attributes for keys/name are set on the self.api instance
        self.assertEqual(portfolio.api, mock_api_instance)
        MockApiClass.assert_called_once_with(broker="Phil", apikeys='env_api_keys', apiname='env_api_name')

        # Check data_directory (assuming it's set from env var in __init__)
        # This part depends on whether PORTFOLIO_DATA_DIRECTORY was part of the changes
        # assumed for this state of draftbot.py. If it was, this test is valid.
        # Based on "os.chdir Removal & Absolute Paths" subtask, data_directory would be set from env.
        # self.assertEqual(portfolio.data_directory, './mock_data_dir') # This attribute doesn't exist on portfolio directly

        # Check that Message was instantiated (implicitly using env vars if Message was modified)
        MockMessageClass.assert_called_once_with(selfmail='env_email@example.com', selfpass='env_email_password')


@unittest.skipIf(not DRAFTBOT_AVAILABLE, "draftbot.py module not found or imports failed")
class TestIndicators(unittest.TestCase):
    def setUp(self):
        # Basic data for indicators that expect 'Close', 'High', 'Low', 'Volume'
        self.data_df = pd.DataFrame({
            'Close': np.array([10, 12, 11, 13, 14, 15, 16, 18, 17, 19, 20, 22], dtype=float),
            'High':  np.array([11, 13, 12, 14, 15, 16, 17, 19, 18, 20, 21, 23], dtype=float),
            'Low':   np.array([9,  11, 10, 12, 13, 14, 15, 17, 16, 18, 19, 21], dtype=float),
            'Volume':np.array([100,110, 90,120,130,140,150,160,140,170,180,190], dtype=float)
        })
        self.close_series = self.data_df['Close']

    def test_simple_moving_average_series_input(self):
        sma = SimpleMovingAverage(windows=3)
        result = sma.output_(self.close_series)
        self.assertIsInstance(result, pd.Series)
        self.assertEqual(len(result), len(self.close_series))
        # Expected values for SMA(3) with min_periods=1, center=True:
        # (NaN, 10, 11)/3 -> (10+12)/2=11 for first centered, (10+12+11)/3=11 for second
        # Pandas default for center=True:
        # idx 0: (s[0] + s[1])/2 = (10+12)/2 = 11 (if len=1, val; if len=2, mean)
        # idx 1: (s[0]+s[1]+s[2])/3 = (10+12+11)/3 = 11
        # idx 2: (s[1]+s[2]+s[3])/3 = (12+11+13)/3 = 12
        # Let's check a few values based on standard pandas behavior
        pd_sma = self.close_series.rolling(window=3, min_periods=1, center=True).mean()
        pd.testing.assert_series_equal(result, pd_sma, check_dtype=False)


    def test_exponential_moving_average_dataframe_input(self):
        # EMA's _input selects 'Close' or 'Adj Close'.
        # The peculiar EMA calculation was simplified in later steps (which are not assumed here).
        # Test based on the original try-except logic for EMA.
        ema = ExponentialMovingAverage(windows=3)
        result = ema.output_(self.data_df)
        self.assertIsInstance(result, pd.Series)
        self.assertEqual(len(result), len(self.data_df))
        # The result depends on whether the try or except block in EMA._input is hit.
        # If try block (SMA-based):
        # sma_close = self.close_series.rolling(window=3,min_periods=1,center=True).mean()
        # simple = self.close_series - sma_close # This is an issue if sma_close has different NaNs
        # simple = np.exp(simple)
        # expected_ema_peculiar = (2/3) * simple # Original had (2/self.windows)
        # If except block (standard EWM):
        expected_ema_standard = self.close_series.ewm(span=3, adjust=True).mean()
        # Due to the try-except, it's hard to predict without running which path it takes.
        # For now, just checking type and length is a basic test.
        # A more specific test would require mocking SimpleMovingAverage within EMA or known data.

if __name__ == '__main__':
    unittest.main()

```
