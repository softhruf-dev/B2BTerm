"""Main helper"""
__docformat__ = "numpy"
import argparse
import json
from datetime import datetime, timedelta
from typing import List, Union

import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd
import pandas_market_calendars as mcal
import plotly.graph_objects as go
import pyEX
import pytz
import requests
import yfinance as yf
from alpha_vantage.timeseries import TimeSeries
from numpy.core.fromnumeric import transpose
from plotly.subplots import make_subplots
from scipy import stats
from tabulate import tabulate

from gamestonk_terminal import config_terminal as cfg
from gamestonk_terminal import feature_flags as gtff
from gamestonk_terminal.helper_funcs import (
    parse_known_args_and_warn,
    plot_autoscale,
    try_except,
    get_user_timezone_or_invalid,
)

# pylint: disable=no-member,too-many-branches,C0302

INTERVALS = [1, 5, 15, 30, 60]
SOURCES = ["yf", "av", "iex"]


@try_except
def search(
    query: str,
    amount: int,
):
    """Search selected query for tickers.

    Parameters
    ----------
    query : str
        The search term used to find company tickers.
    amount : int
        The amount of companies shown.

    Returns
    -------
    tabulate
        Companies that match the query.
    """
    equities_list = (
        "https://raw.githubusercontent.com/JerBouma/FinanceDatabase/master/"
        "Database/Equities/Equities List.json"
    )
    request = requests.get(equities_list)
    equities = json.loads(request.text)

    equities_query = {
        key: value
        for key, value in equities.items()
        if (query in key.lower()) or (query in value.lower())
    }

    equities_dataframe = pd.DataFrame(
        equities_query.items(),
        index=equities_query.values(),
        columns=["Company", "Ticker"],
    )

    if equities_dataframe.empty:
        raise ValueError("No companies found. \n")

    if gtff.USE_TABULATE_DF:
        print(
            tabulate(
                equities_dataframe.iloc[:amount],
                showindex=False,
                headers=["Company", "Ticker"],
                tablefmt="fancy_grid",
            ),
            "\n",
        )
    else:
        print(equities_dataframe.iloc[:amount].to_string(), "\n")


@try_except
def load(
    ticker: str,
    start: datetime = (datetime.now() - timedelta(days=366)),
    interval: int = 1440,
    end: datetime = datetime.now(),
    prepost: bool = False,
    source: str = "yf",
    iexrange: str = "ytd",
):
    """
    Load a symbol to perform analysis using the string above as a template. Optional arguments and their
    descriptions are listed above. The default source is, yFinance (https://pypi.org/project/yfinance/).
    Alternatively, one may select either AlphaVantage (https://www.alphavantage.co/documentation/)
    or IEX Cloud (https://iexcloud.io/docs/api/) as the data source for the analysis.
    Please note that certain analytical features are exclusive to the source.

    To load a symbol from an exchange outside of the NYSE/NASDAQ default, use yFinance as the source and
    add the corresponding exchange to the end of the symbol. i.e. ‘BNS.TO’.

    BNS is a dual-listed stock, there are separate options chains and order books for each listing.
    Opportunities for arbitrage may arise from momentary pricing discrepancies between listings
    with a dynamic exchange rate as a second order opportunity in ForEx spreads.

    Find the full list of supported exchanges here:
    https://help.yahoo.com/kb/exchanges-data-providers-yahoo-finance-sln2310.html

    Certain analytical features, such as VWAP, require the ticker to be loaded as intraday
    using the ‘-i x’ argument.  When encountering this error, simply reload the symbol using
    the interval argument. i.e. ‘load -t BNS -s YYYY-MM-DD -i 1 -p’ loads one-minute intervals,
    including Pre/After Market data, using the default source, yFinance.

    Certain features, such as the Prediction menu, require the symbol to be loaded as daily and not intraday.

    Parameters
    ----------
    ticker: str
        Ticker to get data
    start: datetime
        Start date to get data from with
    interval: int
        Interval (in minutes) to get data 1, 5, 15, 30, 60 or 1440
    end: datetime
        End date to get data from with
    prepost: bool
        Pre and After hours data
    source: str
        Source of data extracted
    iexrange: str
        Timeframe to get IEX data.

    Returns
    -------
    df_stock_candidate: pd.DataFrame
        Dataframe of data
    """

    # Daily
    if interval == 1440:

        # Alpha Vantage Source
        if source == "av":
            ts = TimeSeries(key=cfg.API_KEY_ALPHAVANTAGE, output_format="pandas")
            # pylint: disable=unbalanced-tuple-unpacking
            df_stock_candidate, _ = ts.get_daily_adjusted(
                symbol=ticker, outputsize="full"
            )

            df_stock_candidate.columns = [
                val.split(". ")[1].capitalize() for val in df_stock_candidate.columns
            ]

            df_stock_candidate = df_stock_candidate.rename(
                columns={
                    "Adjusted close": "Adj Close",
                }
            )

            # Check that loading a stock was not successful
            # pylint: disable=no-member
            if df_stock_candidate.empty:
                return pd.DataFrame()

            df_stock_candidate.index = df_stock_candidate.index.tz_localize(None)

            # pylint: disable=no-member
            df_stock_candidate.sort_index(ascending=True, inplace=True)

            # Slice dataframe from the starting date YYYY-MM-DD selected
            df_stock_candidate = df_stock_candidate[
                (df_stock_candidate.index >= start.strftime("%Y-%m-%d"))
                & (df_stock_candidate.index <= end.strftime("%Y-%m-%d"))
            ]

        # Yahoo Finance Source
        elif source == "yf":
            df_stock_candidate = yf.download(
                ticker,
                start=start,
                end=end,
                progress=False,
            )

            # Check that loading a stock was not successful
            if df_stock_candidate.empty:
                return pd.DataFrame()

            df_stock_candidate.index.name = "date"

        # IEX Cloud Source
        elif source == "iex":
            client = pyEX.Client(api_token=cfg.API_IEX_TOKEN, version="v1")

            df_stock_candidate = client.chartDF(ticker, timeframe=iexrange)

            # Check that loading a stock was not successful
            if df_stock_candidate.empty:
                return pd.DataFrame()

            df_stock_candidate = df_stock_candidate[
                ["close", "fHigh", "fLow", "fOpen", "fClose", "volume"]
            ]
            df_stock_candidate = df_stock_candidate.rename(
                columns={
                    "close": "Close",
                    "fHigh": "High",
                    "fLow": "Low",
                    "fOpen": "Open",
                    "fClose": "Adj Close",
                    "volume": "Volume",
                }
            )

            df_stock_candidate.sort_index(ascending=True, inplace=True)
        s_start = df_stock_candidate.index[0]
        s_interval = f"{interval}min"

    else:

        s_int = str(interval) + "m"
        s_interval = s_int + "in"
        d_granularity = {"1m": 6, "5m": 59, "15m": 59, "30m": 59, "60m": 729}

        s_start_dt = datetime.utcnow() - timedelta(days=d_granularity[s_int])
        s_date_start = s_start_dt.strftime("%Y-%m-%d")

        df_stock_candidate = yf.download(
            ticker,
            start=s_date_start if s_start_dt > start else start.strftime("%Y-%m-%d"),
            progress=False,
            interval=s_int,
            prepost=prepost,
        )

        # Check that loading a stock was not successful
        if df_stock_candidate.empty:
            return pd.DataFrame()

        df_stock_candidate.index = df_stock_candidate.index.tz_localize(None)

        if s_start_dt > start:
            s_start = pytz.utc.localize(s_start_dt)
        else:
            s_start = start

        df_stock_candidate.index.name = "date"

    s_intraday = (f"Intraday {s_interval}", "Daily")[interval == 1440]

    print(
        f"Loading {s_intraday} {ticker.upper()} stock "
        f"with starting period {s_start.strftime('%Y-%m-%d')} for analysis."
    )

    return df_stock_candidate


def display_candle(
    s_ticker: str, df_stock: pd.DataFrame, use_matplotlib: bool, intraday: bool = False
):
    """Shows candle plot of loaded ticker. [Source: Yahoo Finance, IEX Cloud or Alpha Vantage]

    Parameters
    ----------
    df_stock: pd.DataFrame
        Stock dataframe
    s_ticker: str
        Ticker name
    use_matplotlib: bool
        Flag to use matplotlib instead of interactive plotly chart
    intraday: bool
        Flag for intraday data for plotly range breaks
    """
    if (df_stock.index[1] - df_stock.index[0]).total_seconds() >= 86400:
        df_stock = find_trendline(df_stock, "OC_High", "high")
        df_stock = find_trendline(df_stock, "OC_Low", "low")

    if use_matplotlib:
        mc = mpf.make_marketcolors(
            up="green",
            down="red",
            edge="black",
            wick="black",
            volume="in",
            ohlc="i",
        )

        s = mpf.make_mpf_style(marketcolors=mc, gridstyle=":", y_on_right=True)

        ap0 = []

        if "OC_High_trend" in df_stock.columns:
            ap0.append(
                mpf.make_addplot(df_stock["OC_High_trend"], color="g"),
            )

        if "OC_Low_trend" in df_stock.columns:
            ap0.append(
                mpf.make_addplot(df_stock["OC_Low_trend"], color="b"),
            )

        if gtff.USE_ION:
            plt.ion()

        mpf.plot(
            df_stock,
            type="candle",
            mav=(20, 50),
            volume=True,
            title=f"\nStock {s_ticker}",
            addplot=ap0,
            xrotation=10,
            style=s,
            figratio=(10, 7),
            figscale=1.10,
            figsize=(plot_autoscale()),
            update_width_config=dict(
                candle_linewidth=1.0, candle_width=0.8, volume_linewidth=1.0
            ),
        )
    else:
        fig = make_subplots(
            rows=2,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.06,
            subplot_titles=(f"{s_ticker}", "Volume"),
            row_width=[0.2, 0.7],
        )
        fig.add_trace(
            go.Candlestick(
                x=df_stock.index,
                open=df_stock.Open,
                high=df_stock.High,
                low=df_stock.Low,
                close=df_stock.Close,
                name="OHLC",
            ),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=df_stock.index,
                y=df_stock["ma20"],
                name="MA20",
                mode="lines",
                line=go.scatter.Line(color="royalblue"),
            ),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Scatter(
                x=df_stock.index,
                y=df_stock["ma50"],
                name="MA50",
                mode="lines",
                line=go.scatter.Line(color="black"),
            ),
            row=1,
            col=1,
        )

        if "OC_High_trend" in df_stock.columns:
            fig.add_trace(
                go.Scatter(
                    x=df_stock.index,
                    y=df_stock["OC_High_trend"],
                    name="High Trend",
                    mode="lines",
                    line=go.scatter.Line(color="green"),
                ),
                row=1,
                col=1,
            )
        if "OC_Low_trend" in df_stock.columns:
            fig.add_trace(
                go.Scatter(
                    x=df_stock.index,
                    y=df_stock["OC_Low_trend"],
                    name="Low Trend",
                    mode="lines",
                    line=go.scatter.Line(color="red"),
                ),
                row=1,
                col=1,
            )

        fig.add_trace(
            go.Bar(
                x=df_stock.index,
                y=df_stock.Volume,
                name="Volume",
                marker_color="#696969",
            ),
            row=2,
            col=1,
        )
        fig.update_layout(
            yaxis_title="Stock Price ($)",
            xaxis=dict(
                rangeselector=dict(
                    buttons=list(
                        [
                            dict(
                                count=1,
                                label="1m",
                                step="month",
                                stepmode="backward",
                            ),
                            dict(
                                count=3,
                                label="3m",
                                step="month",
                                stepmode="backward",
                            ),
                            dict(count=1, label="YTD", step="year", stepmode="todate"),
                            dict(
                                count=1,
                                label="1y",
                                step="year",
                                stepmode="backward",
                            ),
                            dict(step="all"),
                        ]
                    )
                ),
                rangeslider=dict(visible=False),
                type="date",
            ),
        )
        if intraday:
            fig.update_xaxes(
                rangebreaks=[
                    dict(bounds=["sat", "mon"]),
                    dict(bounds=[16, 9.5], pattern="hour"),
                ]
            )

        fig.show()
    print("")


def quote(other_args: List[str], s_ticker: str):
    """Ticker quote

    Parameters
    ----------
    other_args : List[str]
        Argparse arguments
    s_ticker : str
        Ticker
    """
    parser = argparse.ArgumentParser(
        add_help=False,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        prog="quote",
        description="Current quote for stock ticker",
    )

    if s_ticker:
        parser.add_argument(
            "-t",
            "--ticker",
            action="store",
            dest="s_ticker",
            default=s_ticker,
            help="Stock ticker",
        )
    else:
        parser.add_argument(
            "-t",
            "--ticker",
            action="store",
            dest="s_ticker",
            required=True,
            help="Stock ticker",
        )

    # Price only option.
    parser.add_argument(
        "-p",
        "--price",
        action="store_true",
        dest="price_only",
        default=False,
        help="Price only",
    )

    try:
        # For the case where a user uses: 'quote BB'
        if other_args and "-" not in other_args[0][0]:
            other_args.insert(0, "-t")
        ns_parser = parse_known_args_and_warn(parser, other_args)
        if not ns_parser:
            return

    except SystemExit:
        print("")
        return

    ticker = yf.Ticker(ns_parser.s_ticker)

    # If price only option, return immediate market price for ticker.
    if ns_parser.price_only:
        print(f"Price of {ns_parser.s_ticker} {ticker.info['regularMarketPrice']} \n")
        return

    try:
        quote_df = pd.DataFrame(
            [
                {
                    "Symbol": ticker.info["symbol"],
                    "Name": ticker.info["shortName"],
                    "Price": ticker.info["regularMarketPrice"],
                    "Open": ticker.info["regularMarketOpen"],
                    "High": ticker.info["dayHigh"],
                    "Low": ticker.info["dayLow"],
                    "Previous Close": ticker.info["previousClose"],
                    "Volume": ticker.info["volume"],
                    "52 Week High": ticker.info["fiftyTwoWeekHigh"],
                    "52 Week Low": ticker.info["fiftyTwoWeekLow"],
                }
            ]
        )

        quote_df["Change"] = quote_df["Price"] - quote_df["Previous Close"]
        quote_df["Change %"] = quote_df.apply(
            lambda x: f'{((x["Change"] / x["Previous Close"]) * 100):.2f}%',
            axis="columns",
        )
        for c in [
            "Price",
            "Open",
            "High",
            "Low",
            "Previous Close",
            "52 Week High",
            "52 Week Low",
            "Change",
        ]:
            quote_df[c] = quote_df[c].apply(lambda x: f"{x:.2f}")
        quote_df["Volume"] = quote_df["Volume"].apply(lambda x: f"{x:,}")

        quote_df = quote_df.set_index("Symbol")

        quote_data = transpose(quote_df)

        print(
            tabulate(
                quote_data,
                headers=quote_data.columns,  # type: ignore
                tablefmt="fancy_grid",
                stralign="right",
            )
        )

    except KeyError:
        print(f"Invalid stock ticker: {ns_parser.s_ticker}")

    print("")
    return


def load_ticker(
    ticker: str, start_date: Union[str, datetime], end_date: Union[str, datetime] = ""
) -> pd.DataFrame:
    """Loads a ticker data from Yahoo Finance, adds a data index column data_id and Open-Close High/Low columns.

    Parameters
    ----------
    ticker : str
        The stock ticker.
    start_date : Union[str,datetime]
        Start date to load stock ticker data formatted YYYY-MM-DD.
    end_date : Union[str,datetime]
        End date to load stock ticker data formatted YYYY-MM-DD.

    Returns
    -------
    DataFrame
        A Panda's data frame with columns Open, High, Low, Close, Adj Close, Volume, date_id, OC-High, OC-Low.
    """
    if end_date:
        df_data = yf.download(ticker, start=start_date, end=end_date, progress=False)
    else:
        df_data = yf.download(ticker, start=start_date, progress=False)

    df_data["date_id"] = (df_data.index.date - df_data.index.date.min()).astype(
        "timedelta64[D]"
    )
    df_data["date_id"] = df_data["date_id"].dt.days + 1

    df_data["OC_High"] = df_data[["Open", "Close"]].max(axis=1)
    df_data["OC_Low"] = df_data[["Open", "Close"]].min(axis=1)

    return df_data


def process_candle(df_data: pd.DataFrame) -> pd.DataFrame:
    """Process DataFrame into candle style plot

    Parameters
    ----------
    df_data : DataFrame
        Stock dataframe.

    Returns
    -------
    DataFrame
        A Panda's data frame with columns Open, High, Low, Close, Adj Close, Volume, date_id, OC-High, OC-Low.
    """
    df_data["date_id"] = (df_data.index.date - df_data.index.date.min()).astype(
        "timedelta64[D]"
    )
    df_data["date_id"] = df_data["date_id"].dt.days + 1

    df_data["OC_High"] = df_data[["Open", "Close"]].max(axis=1)
    df_data["OC_Low"] = df_data[["Open", "Close"]].min(axis=1)

    df_data["ma20"] = df_data["Close"].rolling(20).mean().fillna(method="bfill")
    df_data["ma50"] = df_data["Close"].rolling(50).mean().fillna(method="bfill")

    return df_data


def find_trendline(
    df_data: pd.DataFrame, y_key: str, high_low: str = "high"
) -> pd.DataFrame:
    """Attempts to find a trend line based on y_key column from a given stock ticker data frame.

    Parameters
    ----------
    df_data : DataFrame
        The stock ticker data frame with at least date_id, y_key columns.
    y_key : str
        Column name to base the trend line on.
    high_low: str, optional
        Either "high" or "low". High is the default.

    Returns
    -------
    DataFrame
        If a trend is successfully found,
            An updated Panda's data frame with a trend data {y_key}_trend column.
        If no trend was found,
            An original Panda's data frame
    """

    for iteration in [3, 4, 5, 6, 7]:
        df_temp = df_data.copy()
        while len(df_temp) > iteration:
            reg = stats.linregress(
                x=df_temp["date_id"],
                y=df_temp[y_key],
            )

            if high_low == "high":
                df_temp = df_temp.loc[
                    df_temp[y_key] > reg[0] * df_temp["date_id"] + reg[1]
                ]
            else:
                df_temp = df_temp.loc[
                    df_temp[y_key] < reg[0] * df_temp["date_id"] + reg[1]
                ]

        if len(df_temp) > 1:
            break

    if len(df_temp) == 1:
        return df_data

    reg = stats.linregress(
        x=df_temp["date_id"],
        y=df_temp[y_key],
    )

    df_data[f"{y_key}_trend"] = reg[0] * df_data["date_id"] + reg[1]

    return df_data


def additional_info_about_ticker(ticker: str) -> str:
    """Additional information about trading the ticker such as exchange, currency, timezone and market status

    Parameters
    ----------
    ticker : str
        The stock ticker to extract if stock market is open or not

    Returns
    -------
    str
        Additional information about trading the ticker
    """
    extra_info = ""
    if ticker:
        ticker_info = yf.Ticker(ticker).info

        extra_info += "\nDatetime: "
        if (
            "exchangeTimezoneName" in ticker_info
            and ticker_info["exchangeTimezoneName"]
        ):
            dtime = datetime.now(
                pytz.timezone(ticker_info["exchangeTimezoneName"])
            ).strftime("%Y %b %d %H:%M")
            extra_info += dtime
            extra_info += "\nTimezone: "
            extra_info += ticker_info["exchangeTimezoneName"]
        else:
            extra_info += "\nDatetime: "
            extra_info += "\nTimezone: "

        extra_info += "\nExchange: "
        if "exchange" in ticker_info and ticker_info["exchange"]:
            exchange_name = ticker_info["exchange"]
            extra_info += exchange_name
            exchange_name = exchange_name.replace("NMS", "NASDAQ")

        extra_info += "\nCurrency: "
        if "currency" in ticker_info and ticker_info["currency"]:
            extra_info += ticker_info["currency"]

        extra_info += "\nMarket:   "
        if "exchange" in ticker_info and ticker_info["exchange"]:
            if exchange_name in mcal.get_calendar_names():
                calendar = mcal.get_calendar(exchange_name)
                sch = calendar.schedule(
                    start_date=(datetime.now() - timedelta(days=3)).strftime(
                        "%Y-%m-%d"
                    ),
                    end_date=(datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d"),
                )
                user_tz = get_user_timezone_or_invalid()
                if user_tz != "INVALID":
                    is_market_open = calendar.open_at_time(
                        sch,
                        pd.Timestamp(
                            datetime.now().strftime("%Y-%m-%d %H:%M"), tz=user_tz
                        ),
                    )
                    if is_market_open:
                        extra_info += "OPEN"
                    else:
                        extra_info += "CLOSED"

    else:
        extra_info += "\nDatetime: "
        extra_info += "\nTimezone: "
        extra_info += "\nExchange: "
        extra_info += "\nMarket: "
        extra_info += "\nCurrency: "

    return extra_info
