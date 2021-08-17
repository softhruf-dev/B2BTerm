"""CoinGecko helpers"""
__docformat__ = "numpy"

import json
import datetime as dt
from datetime import timezone
from typing import Sequence, Optional, Any, Dict, Tuple, Union
import textwrap
import requests
from bs4 import BeautifulSoup
import pandas as pd
from dateutil import parser


GECKO_BASE_URL = "https://www.coingecko.com"

DENOMINATION = ("usd", "btc", "eth")


def get_btc_price() -> float:
    """Get BTC/USD price from CoinGecko API

    Returns
    -------
    str
        latest bitcoin price in usd.
    """
    req = requests.get(
        "https://api.coingecko.com/api/v3/simple/"
        "price?ids=bitcoin&vs_currencies=usd&include_market_cap"
        "=false&include_24hr_vol"
        "=false&include_24hr_change=false&include_last_updated_at=false"
    )
    return req.json()["bitcoin"]["usd"]


def scrape_gecko_data(url: str) -> BeautifulSoup:
    """Helper method that scrape Coin Gecko site.

    Parameters
    ----------
    url : str
        coin gecko url to scrape e.g: "https://www.coingecko.com/en/discover"

    Returns
    -------
        BeautifulSoup object
    """

    req = requests.get(url)
    return BeautifulSoup(req.text, features="lxml")


def replace_underscores_to_newlines(cols: list, line: int = 13) -> list:
    """Helper method that replace underscores to white space and breaks it to new line

    Parameters
    ----------
    cols
        - list of columns names
    line
        - line length
    Returns
    -------
        list of column names with replaced underscores
    """
    return [
        textwrap.fill(c.replace("_", " "), line, break_long_words=False)
        for c in list(cols)
    ]


def find_discord(item: list) -> Union[str, Any]:
    if isinstance(item, list) and len(item) > 0:
        discord = [chat for chat in item if "discord" in chat]
        if len(discord) > 0:
            return discord[0]
    return None


def join_list_elements(elem):
    if isinstance(elem, dict):
        return ", ".join(k for k, v in elem.items())
    if isinstance(elem, list):
        return ", ".join(k for k in elem)
    return None


def filter_list(lst: list) -> list:
    if isinstance(lst, list) and len(lst) > 0:
        return [i for i in lst if i != ""]
    return lst


def calculate_time_delta(date: dt.datetime) -> int:
    now = dt.datetime.now(timezone.utc)
    if not isinstance(date, dt.datetime):
        date = parser.parse(date)
    return (now - date).days


def get_eth_addresses_for_cg_coins(file) -> pd.DataFrame:  # pragma: no cover
    with open(file) as f:
        data = json.load(f)
        df = pd.DataFrame(data)
        df["ethereum"] = df["platforms"].apply(
            lambda x: x.get("ethereum") if "ethereum" in x else None
        )
        return df


def clean_question_marks(dct: dict) -> None:
    if isinstance(dct, dict):
        for k, v in dct.items():
            if v == "?":
                dct[k] = None


def replace_qm(df: pd.DataFrame) -> pd.DataFrame:
    df.replace({"?": None, " ?": None}, inplace=True)
    return df


def get_url(url: str, elem: BeautifulSoup):  # pragma: no cover
    return url + elem.find("a")["href"]


def clean_row(row):
    """Helper method that cleans whitespaces and newlines in text returned from BeautifulSoup
    Parameters
    ----------
    row
        text returned from BeautifulSoup find method
    Returns
    -------
        list of elements

    """
    return [r for r in row.text.strip().split("\n") if r not in ["", " "]]


def convert(word):
    return "".join(x.capitalize() or "_" for x in word.split("_") if word.isalpha())


def collateral_auditors_parse(args):  # pragma: no cover
    try:
        if args and args[0] == "N/A":
            collateral = args[1:]
            auditors = []
        else:
            n_elem = int(args[0])
            auditors = args[1 : n_elem + 1]
            collateral = args[n_elem + 1 :]

        return auditors, collateral
    except ValueError:
        return [], []


def swap_columns(df):
    cols = list(df.columns)
    cols = [cols[-1]] + cols[:-1]
    df = df[cols]
    return df


def changes_parser(changes):
    if isinstance(changes, list) and len(changes) < 3:
        for _ in range(3 - len(changes)):
            changes.append(None)
    else:
        changes = [None for _ in range(3)]
    return changes


def remove_keys(entries, the_dict):
    for key in entries:
        if key in the_dict:
            del the_dict[key]


def rename_columns_in_dct(dct, mapper):
    return {mapper.get(k, v): v for k, v in dct.items()}


def create_dictionary_with_prefixes(
    columns: Sequence[Any], dct: Dict[Any, Any], constrains: Optional[Tuple] = None
):  # type: ignore
    results = {}
    for column in columns:
        ath_data = dct.get(column)
        for element in ath_data:  # type: ignore
            if constrains:  # type: ignore
                if element in constrains:  # type: ignore
                    results[f"{column}_" + element] = ath_data.get(element)  # type: ignore
            else:
                results[f"{column}_" + element] = ath_data.get(element)  # type: ignore
    return results
