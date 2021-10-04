"""Ark Model"""
__docformat__ = "numpy"

import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
from gamestonk_terminal.helper_funcs import get_user_agent


def get_ark_trades_by_ticker(ticker: str) -> pd.DataFrame:
    """Gets a dataframe of ARK trades for ticker

    Parameters
    ----------
    ticker : str
        Ticker to get trades for

    Returns
    -------
    pd.DataFrame
        DataFrame of trades
    """
    url = f"https://cathiesark.com/ark-combined-holdings-of-{ticker}"
    r = requests.get(url, headers={"User-Agent": get_user_agent()})
    parsed_script = BeautifulSoup(r.text, "lxml").find(
        "script", {"id": "__NEXT_DATA__"}
    )
    parsed_json = json.loads(parsed_script.string)
    df_orders = pd.json_normalize(parsed_json["props"]["pageProps"]["trades"])
    df_orders = df_orders.drop(columns=["hidden", "everything.profile.customThumbnail"])
    df_orders["date"] = df_orders["date"].apply(lambda x: x.strip("Z"))
    return df_orders
