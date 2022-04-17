""" Comparison Analysis FinBrain Model """
__docformat__ = "numpy"

import logging
from typing import List

import pandas as pd
import requests

from openbb_terminal.decorators import log_start_end
from openbb_terminal.rich_config import console

logger = logging.getLogger(__name__)


@log_start_end(log=logger)
def get_sentiments(tickers: List[str]) -> pd.DataFrame:
    """Gets Sentiment analysis from several tickers provided by FinBrain's API

    Parameters
    ----------
    tickers : List[str]
        List of tickers to get sentiment

    Returns
    -------
    pd.DataFrame
        Contains sentiment analysis from several tickers
    """

    df_sentiment = pd.DataFrame()
    dates_sentiment = []
    tickers_to_remove = list()
    for ticker in tickers:
        result = requests.get(f"https://api.finbrain.tech/v0/sentiments/{ticker}")
        if result.status_code == 200:
            result_json = result.json()
            if "ticker" in result_json and "sentimentAnalysis" in result_json:
                df_sentiment[ticker] = [
                    float(val)
                    for val in list(result_json["sentimentAnalysis"].values())
                ]
                dates_sentiment = list(result_json["sentimentAnalysis"].keys())
            else:
                console.print(f"Unexpected data format from FinBrain API for {ticker}")
                tickers_to_remove.append(ticker)

        else:
            console.print(
                f"Request error in retrieving {ticker} sentiment from FinBrain API"
            )
            tickers_to_remove.append(ticker)

    for ticker in tickers_to_remove:
        tickers.remove(ticker)

    if not df_sentiment.empty:
        df_sentiment.index = dates_sentiment
        df_sentiment.sort_index(ascending=True, inplace=True)

    return df_sentiment
