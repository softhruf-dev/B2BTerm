from unittest import mock, TestCase
import json
import os

import vcr
from pycoingecko import CoinGeckoAPI

from openbb_terminal.cryptocurrency.cryptocurrency_helpers import (
    plot_chart,
    load,
    load_ta_data,
    prepare_all_coins_df,
)
from tests.helpers.helpers import check_print

# pylint: disable=unused-import


@mock.patch(
    "openbb_terminal.cryptocurrency.due_diligence.pycoingecko_model.CoinGeckoAPI.get_coin_market_chart_by_id"
)
def get_bitcoin(mock_load):
    # pylint: disable=unused-argument
    print(os.getcwd())

    with open(
        "tests/openbb_terminal/cryptocurrency/json/test_cryptocurrency_helpers/btc_usd_test_data.json",
        encoding="utf8",
    ) as f:
        sample_return = json.load(f)
    mock_load.return_value = sample_return
    coin, _, symbol, _, _, _ = load(coin="BTC", source="cp")
    return coin, symbol


# pylint: disable=R0904
class TestCoinGeckoAPI(TestCase):
    # pylint: disable = no-value-for-parameter
    coin, symbol = get_bitcoin()

    coin_map_df = prepare_all_coins_df().set_index("Symbol").loc[symbol.upper()].iloc[0]

    def test_coin_api_load(self):
        """
        Mock load function through get_coin_market_chart_by_id.
        Mock returns a dict saved as .json
        """
        self.assertEqual(self.coin, "btc-bitcoin")

    @mock.patch(
        "openbb_terminal.cryptocurrency.due_diligence.pycoingecko_model.CoinGeckoAPI.get_coin_market_chart_by_id"
    )
    def test_coin_api_load_df_for_ta(self, mock_load):
        """
        Mock load function through get_coin_market_chart_by_id.
        Mock returns a dict saved as .json
        """

        with open(
            "tests/openbb_terminal/cryptocurrency/json/test_cryptocurrency_helpers/btc_usd_test_data.json",
            encoding="utf8",
        ) as f:
            sample_return = json.load(f)

        mock_load.return_value = sample_return
        mock_return, vs = load_ta_data(
            coin_map_df=self.coin_map_df,
            source="cg",
            currency="usd",
            days=30,
        )
        self.assertTrue(mock_return.shape == (31, 4))
        self.assertTrue(vs == "usd")

    @check_print()
    @vcr.use_cassette(
        "tests/openbb_terminal/cryptocurrency/cassettes/test_cryptocurrency_helpers/test_get_coins.yaml",
        record_mode="new_episodes",
    )
    def test_get_coins(self):
        """Test that pycoingecko retrieves the major coins"""
        coins = CoinGeckoAPI().get_coins()
        bitcoin_list = [coin["id"] for coin in coins]
        test_coins = ["bitcoin", "ethereum", "dogecoin"]
        for test in test_coins:
            self.assertIn(test, bitcoin_list)

    @check_print(assert_in="\n")
    @mock.patch("matplotlib.pyplot.show")
    def test_coin_chart(self, mock_matplot):
        # pylint: disable=unused-argument
        plot_chart(coin_map_df=self.coin_map_df, source="cg", currency="usd", days=30)

    # TODO: Re-add tests for coin_list and find
