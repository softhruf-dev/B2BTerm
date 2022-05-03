from datetime import datetime
from typing import List, Optional, Dict
import os
import argparse
import logging

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf

from openbb_terminal.forex import av_model
from openbb_terminal.rich_config import console
from openbb_terminal.decorators import log_start_end
from openbb_terminal.helper_funcs import plot_autoscale
from openbb_terminal.config_terminal import theme


FOREX_SOURCES: Dict = {
    "yf": "YahooFinance",
    "av": "AlphaAdvantage",
    "oanda": "Oanda",
}

SOURCES_INTERVALS: Dict = {
    "yf": [
        "1min",
        "2min",
        "5min",
        "15min",
        "30min",
        "60min",
        "90min",
        "1hour",
        "1day",
        "5day",
        "1week",
        "1month",
        "3month",
    ],
    "av": ["1min", "5min", "15min", "30min", "60min"],
}

INTERVAL_MAPS: Dict = {
    "yf": {
        "1min": "1m",
        "2min": "2m",
        "5min": "5m",
        "15min": "15m",
        "30min": "30m",
        "60min": "60m",
        "90min": "90m",
        "1hour": "1h",
        "1day": "1d",
        "5day": "5d",
        "1week": "1wk",
        "1month": "1mo",
        "3month": "3mo",
    },
    "av": {"1min": 1, "5min": 5, "15min": 15, "30min": 30, "60min": 60},
}

logger = logging.getLogger(__name__)


@log_start_end(log=logger)
def load(
    to_symbol: str,
    from_symbol: str,
    resolution: str,
    interval: str,
    start_date: str,
    source: str = "yf",
):
    interval_map = INTERVAL_MAPS[source]

    if interval not in interval_map.keys():
        console.print(
            f"Interval not supported by {FOREX_SOURCES[source]}. Need to be one of the following options",
            interval_map.keys(),
        )
        return pd.DataFrame()

    if source == "av":

        df = av_model.get_historical(
            to_symbol=to_symbol,
            from_symbol=from_symbol,
            resolution=resolution,
            interval=interval_map[interval],
            start_date=start_date,
        )

    if source == "yf":

        df = yf.download(
            f"{from_symbol}{to_symbol}=X",
            end=datetime.now(),
            start=datetime.strptime(start_date, "%Y-%m-%d"),
            interval=interval_map[interval],
            progress=False,
        )

    return df


@log_start_end(log=logger)
def get_yf_currency_list() -> List:
    """Load YF list of forex pair a local file."""
    path = os.path.join(os.path.dirname(__file__), "data/yahoofinance_forex.json")

    return sorted(list(set(pd.read_json(path)["from_symbol"])))


YF_CURRENCY_LIST = get_yf_currency_list()


@log_start_end(log=logger)
def check_valid_yf_forex_currency(fx_symbol: str) -> str:
    """Check if given symbol is supported on Yahoo Finance

    Parameters
    ----------
    fx_symbol : str
        Symbol to check

    Returns
    -------
    str
        Currency symbol

    Raises
    ------
    argparse.ArgumentTypeError
        Symbol not valid on YahooFinance
    """
    if fx_symbol.upper() in get_yf_currency_list():
        return fx_symbol.upper()

    raise argparse.ArgumentTypeError(
        f"{fx_symbol.upper()} not found in YahooFinance supported currency codes. "
    )


@log_start_end(log=logger)
def display_candle(
    data: pd.DataFrame,
    to_symbol: str,
    from_symbol: str,
    external_axes: Optional[List[plt.Axes]] = None,
):
    """Show candle plot for fx data.

    Parameters
    ----------
    data : pd.DataFrame
        Loaded fx historical data
    to_symbol : str
        To forex symbol
    from_symbol : str
        From forex symbol
    external_axes: Optional[List[plt.Axes]]
        External axes (1 axis are expected in the list), by default None
    """
    candle_chart_kwargs = {
        "type": "candle",
        "style": theme.mpf_style,
        "mav": (20, 50),
        "volume": False,
        "xrotation": theme.xticks_rotation,
        "scale_padding": {"left": 0.3, "right": 1, "top": 0.8, "bottom": 0.8},
        "update_width_config": {
            "candle_linewidth": 0.6,
            "candle_width": 0.8,
            "volume_linewidth": 0.8,
            "volume_width": 0.8,
        },
        "warn_too_much_data": 20000,
    }
    # This plot has 2 axes
    if not external_axes:
        candle_chart_kwargs["returnfig"] = True
        candle_chart_kwargs["figratio"] = (10, 7)
        candle_chart_kwargs["figscale"] = 1.10
        candle_chart_kwargs["figsize"] = plot_autoscale()
        fig, ax = mpf.plot(data, **candle_chart_kwargs)
        fig.suptitle(
            f"{from_symbol}/{to_symbol}",
            x=0.055,
            y=0.965,
            horizontalalignment="left",
        )
        theme.visualize_output(force_tight_layout=False)
        ax[0].legend()
    else:
        if len(external_axes) != 1:
            logger.error("Expected list of 1 axis items.")
            console.print("[red]Expected list of 1 axis items.\n[/red]")
            return
        (ax1,) = external_axes
        candle_chart_kwargs["ax"] = ax1
        mpf.plot(data, **candle_chart_kwargs)
