"""SentimentInvestor View"""
__docformat__ = "numpy"

import logging
import os
from typing import Optional, List
from datetime import datetime
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd

from openbb_terminal.config_terminal import theme
from openbb_terminal.config_plot import PLOT_DPI
from openbb_terminal.rich_config import console
from openbb_terminal.common.behavioural_analysis import sentimentinvestor_model
from openbb_terminal.decorators import log_start_end
from openbb_terminal.decorators import check_api_key
from openbb_terminal.helper_funcs import (
    export_data,
    print_rich_table,
    plot_autoscale,
)


logger = logging.getLogger(__name__)


@log_start_end(log=logger)
@check_api_key(["API_SENTIMENTINVESTOR_TOKEN"])
def display_historical(
    ticker: str,
    start: str,
    end: str,
    export: str = "",
    number: int = 100,
    raw: bool = False,
    limit: int = 10,
    external_axes: Optional[List[plt.Axes]] = None,
):
    """Display historical sentiment data of a ticker,
    and plot a chart with RHI and AHI.

    Parameters
    ----------
    ticker: str
        Ticker to view sentiment data
    start: str
        Initial date like string or unix timestamp (e.g. 2021-12-21)
    end: str
        End date like string or unix timestamp (e.g. 2022-01-15)
    number : int
        Number of results returned by API call
        Maximum 250 per api call
    raw: boolean
        Whether to display raw data, by default False
    limit: int
        Number of results display on the terminal
        Default: 10
    external_axes : Optional[List[plt.Axes]], optional
        External axes (2 axis is expected in the list), by default None
    Returns
    -------
    """

    supported_ticker = sentimentinvestor_model.check_supported_ticker(ticker)

    # Check to see if the ticker is supported
    if not supported_ticker:
        logger.error("Ticker not supported")
        console.print(
            f"[red]Ticker {ticker} not supported. Please try another one![/red]\n"
        )
        return

    df = sentimentinvestor_model.get_historical(ticker, start, end, number)

    if df.empty:
        return

    # This plot has 2 axis
    if external_axes is None:
        _, ax1 = plt.subplots(figsize=plot_autoscale(), dpi=PLOT_DPI)
        ax2 = ax1.twinx()
    else:
        if len(external_axes) != 2:
            logger.error("Expected list of two axis items.")
            console.print("[red]Expected list of 2 axis item.[/red]\n")
            return
        (ax1, ax2) = external_axes

    ax1.plot(df.index, df["RHI"], color=theme.get_colors()[0])

    ax2.plot(df.index, df["AHI"], color=theme.get_colors(reverse=True)[0])

    ax1.set_ylabel("RHI")
    ax1.set_title("Hourly-level data of RHI and AHI")
    ax1.set_xlim(df.index[0], df.index[-1])
    theme.style_primary_axis(ax1)
    ax1.yaxis.set_label_position("left")

    ax2.set_ylabel("AHI")

    theme.style_primary_axis(ax2)
    ax2.yaxis.set_label_position("right")
    ax2.grid(visible=False)

    # Manually construct the chart legend
    colors = [theme.get_colors()[0], theme.get_colors(reverse=True)[0]]
    lines = [Line2D([0], [0], color=c) for c in colors]
    labels = ["RHI", "AHI"]
    ax2.legend(lines, labels)

    if external_axes is None:
        theme.visualize_output()

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)).replace("common", "stocks"),
        "hist",
        df,
    )

    RAW_COLS = ["twitter", "stocktwits", "yahoo", "likes", "RHI", "AHI"]

    if raw:
        df.index = df.index.strftime("%Y-%m-%d %H:%M")
        df.index.name = "Time"

        print_rich_table(
            df[RAW_COLS].head(limit),
            headers=[
                "Twitter",
                "Stocktwits",
                "Yahoo",
                "Likes",
                "RHI",
                "AHI",
            ],
            show_index=True,
            index_name="Time",
            title="Historical Sentiment Data",
        )


@log_start_end(log=logger)
@check_api_key(["API_SENTIMENTINVESTOR_TOKEN"])
def display_trending(
    start: datetime,
    hour: int,
    export: str = "",
    number: int = 10,
    limit: int = 10,
):
    """Display most talked about tickers within
    the last hour together with their sentiment data.

    Parameters
    ----------
    start: datetime
        Datetime object (e.g. datetime(2021, 12, 21)
    hour: int
        Hour of the day in 24-hour notation (e.g. 14)
    number : int
        Number of results returned by API call
        Maximum 250 per api call
    limit: int
        Number of results display on the terminal
        Default: 10
    -------
    Returns
        None
    """

    df = sentimentinvestor_model.get_trending(start, hour, number)

    if df.empty:
        return

    export_data(
        export,
        os.path.dirname(os.path.abspath(__file__)).replace("common", "stocks"),
        "trend",
        df,
    )

    RAW_COLS = [
        "total",
        "twitter",
        "stocktwits",
        "yahoo",
        "likes",
        "RHI",
        "AHI",
    ]

    RAW_COLS = [col for col in RAW_COLS if col in df.columns.tolist()]

    df.ticker = df.ticker.str.upper()
    df = df.set_index("ticker")

    df.timestamp_date = pd.to_datetime(df.timestamp_date)
    timestamp = df.timestamp_date[0].strftime("%Y-%m-%d %H:%M")

    print_rich_table(
        df[RAW_COLS].head(limit),
        headers=[col.upper() for col in RAW_COLS],
        show_index=True,
        index_name="TICKER",
        title=f"Most trending stocks at {timestamp}",
    )
