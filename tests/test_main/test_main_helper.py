import sys
import unittest
from contextlib import contextmanager
from datetime import datetime, timedelta
from unittest.mock import patch

import pandas as pd
import vcr

from gamestonk_terminal import terminal_helper
from gamestonk_terminal.stocks import stocks_helper
from tests.helpers import check_print


def return_val(x, shell, check):
    # pylint: disable=unused-argument
    # pylint: disable=R0903
    class ReturnVal:
        def __init__(self, code):
            self.returncode = code

    return ReturnVal(2)


@contextmanager
def replace_stdin(target):
    orig = sys.stdin
    sys.stdin = target
    yield
    sys.stdin = orig


class TestMainHelper(unittest.TestCase):
    start = datetime.now() - timedelta(days=200)

    # @vcr.use_cassette(
    #     "tests/cassettes/test_main/test_main_helper/general1.yaml",
    #     record_mode="new_episodes",
    # )
    # @check_print(assert_in="Loading Daily GME")
    # def test_load(self):
    #     values = stocks_helper.load(
    #         ["GME"], "GME", self.start, "1440min", pd.DataFrame()
    #     )
    #     self.assertEqual(values[0], "GME")
    #     self.assertNotEqual(values[1], None)
    #     self.assertEqual(values[2], "1440min")

    @check_print()
    def test_load_clear(self):
        stocks_helper.load(["GME"], "GME", self.start, "1440min", pd.DataFrame())
        values = stocks_helper.clear([], "GME", self.start, "1440min", pd.DataFrame())
        self.assertEqual(values[0], "")
        self.assertEqual(values[1], "")
        self.assertEqual(values[2], "")

    # @check_print()
    # @vcr.use_cassette(
    #     "tests/cassettes/test_main/test_main_helper/general1.yaml",
    #     record_mode="new_episodes",
    # )
    # @patch("matplotlib.pyplot.show")
    # def test_candle(self, mock):
    #     # pylint: disable=unused-argument
    #     stocks_helper.candle("GME", [])

    @check_print(assert_in="Price")
    @vcr.use_cassette(
        "tests/cassettes/test_main/test_main_helper/test_quote.yaml",
        record_mode="new_episodes",
    )
    def test_quote(self):
        stocks_helper.quote(["GME"], "GME")

    @check_print()
    @patch("matplotlib.pyplot.show")
    def test_view(self, mock):
        # pylint: disable=unused-argument
        stocks_helper.view(["GME"], "GME", "1440min", pd.DataFrame())

    @check_print(assert_in="ALPHA")
    @vcr.use_cassette(
        "tests/cassettes/test_main/test_main_helper/test_check_api_keys.yaml",
        record_mode="new_episodes",
    )
    def test_check_api_keys(self):
        terminal_helper.check_api_keys()

    @check_print(length=0)
    def test_print_goodbye(self):
        terminal_helper.print_goodbye()

    @patch("subprocess.run", side_effect=return_val)
    def test_update_terminal(self, mock):
        # pylint: disable=unused-argument
        value = terminal_helper.update_terminal()
        self.assertEqual(value, 2)

    @check_print(assert_in="Thanks for using Gamestonk Terminal.")
    def test_about_us(self):
        terminal_helper.about_us()

    @check_print(assert_in="Welcome to Gamestonk Terminal Beta")
    def test_bootup(self):
        terminal_helper.bootup()

    @check_print(assert_in="Unfortunately, resetting wasn't")
    @patch("subprocess.run", side_effect=return_val)
    def test_reset(self, mock):
        # pylint: disable=unused-argument
        terminal_helper.reset()
