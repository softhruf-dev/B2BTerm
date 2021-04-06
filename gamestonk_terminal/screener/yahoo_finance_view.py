import argparse
from typing import List
from pandas.plotting import register_matplotlib_converters
import matplotlib.pyplot as plt
import datetime
import configparser
import yfinance as yf
from finvizfinance.screener import ticker
from gamestonk_terminal.screener import finviz_view

from gamestonk_terminal.helper_funcs import (
    parse_known_args_and_warn,
    plot_autoscale,
    valid_date,
)
from gamestonk_terminal.config_plot import PLOT_DPI

register_matplotlib_converters()

d_candle_types = {
    "o": "Open",
    "h": "High",
    "l": "Low",
    "c": "Close",
    "a": "Adj Close",
}


def check_one_of_ohlca(type_candles: str) -> str:
    if (
        type_candles == "o"
        or type_candles == "h"
        or type_candles == "l"
        or type_candles == "c"
        or type_candles == "a"
    ):
        return type_candles
    raise argparse.ArgumentTypeError("The type of candles specified is not recognized")


def historical(other_args: List[str], preset_loaded: str):
    """View historical price of stocks that meet preset

    Parameters
    ----------
    other_args : List[str]
        Command line arguments to be processed with argparse
    ticker : str
        Loaded preset filter
    """
    parser = argparse.ArgumentParser(
        add_help=False,
        prog="historical",
        description="""Historical price comparison between similar companies [Source: Yahoo Finance]
        """,
    )
    parser.add_argument(
        "--start",
        type=valid_date,
        default=datetime.datetime.now() - datetime.timedelta(days=6 * 30),
        dest="start",
        help="The starting date (format YYYY-MM-DD) of the historical price to plot",
    )
    parser.add_argument(
        "-t",
        "--type",
        action="store",
        dest="type_candle",
        type=check_one_of_ohlca,
        default="a",  # in case it's adjusted close
        help=("type of candles: o-open, h-high, l-low, c-close, a-adjusted close."),
    )
    parser.add_argument(
        "-s",
        "--signal",
        action="store",
        dest="signal",
        type=str,
        default=None,
        help="Signal",
        choices=list(finviz_view.d_signals.keys()),
    )

    try:
        ns_parser = parse_known_args_and_warn(parser, other_args)
        if not ns_parser:
            return

        preset_filter = configparser.RawConfigParser()
        preset_filter.optionxform = str  # type: ignore
        preset_filter.read(
            "gamestonk_terminal/screener/presets/" + preset_loaded + ".ini"
        )

        d_general = preset_filter["General"]
        d_filters = {
            **preset_filter["Descriptive"],
            **preset_filter["Fundamental"],
            **preset_filter["Technical"],
        }

        d_filters = {k: v for k, v in d_filters.items() if v}

        screen = ticker.Ticker()

        if ns_parser.signal:
            screen.set_filter(signal=finviz_view.d_signals[ns_parser.signal])
        else:
            if d_general["Signal"]:
                screen.set_filter(filters_dict=d_filters, signal=d_general["Signal"])
            else:
                screen.set_filter(filters_dict=d_filters)

        l_min = list()
        l_leg = list()
        plt.figure(figsize=plot_autoscale(), dpi=PLOT_DPI)

        l_stocks = screen.ScreenerView(verbose=0)

        if len(l_stocks) > 10:
            print(
                "We limit stocks shown to 10, as after this the plot becomes too noisy. "
                "Also, we ran out of different colors."
            )
            l_stocks = l_stocks[:10]

        while l_stocks:
            l_parsed_stocks = list()
            for symbol in l_stocks:
                try:
                    df_similar_stock = yf.download(
                        symbol,
                        start=datetime.datetime.strftime(ns_parser.start, "%Y-%m-%d"),
                        progress=False,
                        threads=False,
                    )
                    if not df_similar_stock.empty:
                        plt.plot(
                            df_similar_stock.index,
                            df_similar_stock[
                                d_candle_types[ns_parser.type_candle]
                            ].values,
                        )
                        l_min.append(df_similar_stock.index[0])
                        l_leg.append(symbol)

                    l_parsed_stocks.append(symbol)
                except Exception as e:
                    print("")
                    print(e)
                    print(
                        "Disregard previous error, which is due to API Rate limits from Yahoo Finance."
                    )
                    print(
                        f"Because we like '{symbol}', and we won't leave without getting data from it."
                    )

            for parsed_stock in l_parsed_stocks:
                l_stocks.remove(parsed_stock)

        if ns_parser.signal:
            plt.title(
                f"Screener Historical Price using {finviz_view.d_signals[ns_parser.signal]} signal"
            )
        else:
            plt.title(f"Screener Historical Price using {preset_loaded} preset")

        plt.xlabel("Time")
        plt.ylabel("Share Price ($)")
        plt.legend(l_leg)
        plt.grid(b=True, which="major", color="#666666", linestyle="-")
        plt.minorticks_on()
        plt.grid(b=True, which="minor", color="#999999", linestyle="-", alpha=0.2)
        # ensures that the historical data starts from same datapoint
        plt.xlim([max(l_min), df_similar_stock.index[-1]])
        plt.show()
        print("")

    except SystemExit:
        print("Similar companies need to be provided", "\n")
    except Exception as e:
        print(e, "\n")
