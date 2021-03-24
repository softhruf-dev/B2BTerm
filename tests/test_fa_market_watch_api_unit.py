""" fundamental_analysis/market_watch_api.py tests """
import unittest
from unittest import mock

# pylint: disable=unused-import
from gamestonk_terminal.test_helper import (  # noqa: F401
    parametrize_from_file,
    pytest_generate_tests,
)

from gamestonk_terminal.fundamental_analysis.market_watch_api import (
    prepare_df_financials,
)

assertions = unittest.TestCase("__init__")


class TestFaMarketWatchApiUnit:
    @mock.patch("gamestonk_terminal.fundamental_analysis.market_watch_api.requests")
    @parametrize_from_file(
        "test_prepare_df_financials",
        "../tests/data/fa_market_watch_api.yaml",
    )
    def test_prepare_df_financials(
        self, mock_request_get, ticker, statement, mock_market_watch, expected_result
    ):
        mock_request_get.get().text = mock_market_watch
        ret = prepare_df_financials(ticker, statement)

        assertions.assertEqual(ret.to_csv(), expected_result)
