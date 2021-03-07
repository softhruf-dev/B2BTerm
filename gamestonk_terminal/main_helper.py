import argparse
from sys import stdout
import pandas as pd
from alpha_vantage.timeseries import TimeSeries

from gamestonk_terminal.helper_funcs import (
    valid_date,
    plot_view_stock,
    parse_known_args_and_warn,
    check_ohlc,
    lett_to_num,
)

from gamestonk_terminal import config_terminal as cfg


def print_help(s_ticker, s_start, s_interval, b_is_market_open):
    """Print help"""
    print("What do you want to do?")
    print("   help        help to see this menu again")
    print("   quit        to abandon the program")
    print("")
    print("   clear       clear a specific stock ticker from analysis")
    print("   load        load a specific stock ticker for analysis")
    print("   view        view and load a specific stock ticker for technical analysis")
    if s_ticker:
        print(
            "   export      export the currently loaded dataframe to a file or stdout"
        )

    s_intraday = (f"Intraday {s_interval}", "Daily")[s_interval == "1440min"]
    if s_ticker and s_start:
        print(f"\n{s_intraday} Stock: {s_ticker} (from {s_start.strftime('%Y-%m-%d')})")
    elif s_ticker:
        print(f"\n{s_intraday} Stock: {s_ticker}")
    else:
        print("\nStock: ?")
    print(f"Market {('CLOSED', 'OPEN')[b_is_market_open]}.")

    print("\nMenus:")
    print(
        "   disc        discover trending stocks, \t e.g. map, sectors, high short interest"
    )
    print("   mill        papermill menu, \t\t\t menu to generate notebook reports")
    print(
        "   sen         sentiment of the market, \t from: reddit, stocktwits, twitter"
    )
    if s_ticker:
        print(
            "   res         research web page,       \t e.g.: macroaxis, yahoo finance, fool"
        )
        print(
            "   fa          fundamental analysis,    \t e.g.: income, balance, cash, earnings"
        )
        print(
            "   ta          technical analysis,      \t e.g.: ema, macd, rsi, adx, bbands, obv"
        )
        print(
            "   dd          in-depth due-diligence,  \t e.g.: news, analyst, shorts, insider, sec"
        )
        print(
            "   pred        prediction techniques,   \t e.g.: regression, arima, rnn, lstm, prophet"
        )
    print("")


def clear(l_args, s_ticker, s_start, s_interval, df_stock):
    parser = argparse.ArgumentParser(
        prog="clear",
        description="""Clear previously loaded stock ticker.""",
    )

    try:
        parse_known_args_and_warn(parser, l_args)
        print("Clearing stock ticker to be used for analysis\n")
        return "", "", "", pd.DataFrame()

    except SystemExit:
        print("")
        return s_ticker, s_start, s_interval, df_stock


def load(l_args, s_ticker, s_start, s_interval, df_stock):
    parser = argparse.ArgumentParser(
        prog="load", description=""" Load a stock in order to perform analysis"""
    )
    parser.add_argument(
        "-t",
        "--ticker",
        action="store",
        dest="s_ticker",
        required=True,
        help="Stock ticker",
    )
    parser.add_argument(
        "-s",
        "--start",
        type=valid_date,
        dest="s_start_date",
        help="The starting date (format YYYY-MM-DD) of the stock",
    )
    parser.add_argument(
        "-i",
        "--interval",
        action="store",
        dest="n_interval",
        type=int,
        default=1440,
        choices=[1, 5, 15, 30, 60],
        help="Intraday stock minutes",
    )

    try:
        ns_parser = parse_known_args_and_warn(parser, l_args)

    except SystemExit:
        print("")
        return [s_ticker, s_start, s_interval, df_stock]

    # Update values:
    s_ticker = ns_parser.s_ticker
    s_start = ns_parser.s_start_date
    s_interval = str(ns_parser.n_interval) + "min"

    try:
        ts = TimeSeries(key=cfg.API_KEY_ALPHAVANTAGE, output_format="pandas")
        # Daily
        if s_interval == "1440min":
            # pylint: disable=unbalanced-tuple-unpacking
            df_stock, _ = ts.get_daily_adjusted(
                symbol=ns_parser.s_ticker, outputsize="full"
            )
        # Intraday
        else:
            # pylint: disable=unbalanced-tuple-unpacking
            df_stock, _ = ts.get_intraday(
                symbol=ns_parser.s_ticker, outputsize="full", interval=s_interval
            )

        df_stock.sort_index(ascending=True, inplace=True)

    except Exception as e:
        print(e)
        print("Either the ticker or the API_KEY are invalids. Try again!")
        return [s_ticker, s_start, s_interval, df_stock]

    s_intraday = (f"Intraday {s_interval}", "Daily")[s_interval == "1440min"]

    if s_start:
        # Slice dataframe from the starting date YYYY-MM-DD selected
        df_stock = df_stock[ns_parser.s_start_date :]
        print(
            f"Loading {s_intraday} {s_ticker} stock with starting period {s_start.strftime('%Y-%m-%d')} for analysis."
        )
    else:
        print(f"Loading {s_intraday} {s_ticker} stock for analysis.")

    print("")
    return [s_ticker, s_start, s_interval, df_stock]


def view(l_args, s_ticker, s_start, s_interval, df_stock):
    parser = argparse.ArgumentParser(
        prog="view",
        description="Visualize historical data of a stock. An alpha_vantage key is necessary.",
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
    parser.add_argument(
        "-s",
        "--start",
        type=valid_date,
        dest="s_start_date",
        default=s_start,
        help="The starting date (format YYYY-MM-DD) of the stock",
    )
    parser.add_argument(
        "-i",
        "--interval",
        action="store",
        dest="n_interval",
        type=int,
        default=0,
        choices=[1, 5, 15, 30, 60],
        help="Intraday stock minutes",
    )
    parser.add_argument(
        "--type",
        action="store",
        dest="type",
        type=check_ohlc,
        default="a",  # in case it's adjusted close
        help=(
            "ohlc corresponds to types: open; high; low; close; "
            "while oc corresponds to types: open; close"
        ),
    )

    try:
        ns_parser = parse_known_args_and_warn(parser, l_args)

    except SystemExit:
        print("")
        return

    # Update values:
    s_ticker = ns_parser.s_ticker

    # A new interval intraday period was given
    if ns_parser.n_interval != 0:
        s_interval = str(ns_parser.n_interval) + "min"

    type_candles = lett_to_num(ns_parser.type)

    try:
        ts = TimeSeries(key=cfg.API_KEY_ALPHAVANTAGE, output_format="pandas")
        # Daily
        if s_interval == "1440min":
            # pylint: disable=unbalanced-tuple-unpacking
            df_stock, _ = ts.get_daily_adjusted(symbol=s_ticker, outputsize="full")
        # Intraday
        else:
            # pylint: disable=unbalanced-tuple-unpacking
            df_stock, _ = ts.get_intraday(
                symbol=s_ticker, outputsize="full", interval=s_interval
            )

    except Exception as e:
        print(e)
        print("Either the ticker or the API_KEY are invalids. Try again!")
        return

    df_stock.sort_index(ascending=True, inplace=True)

    # Slice dataframe from the starting date YYYY-MM-DD selected
    df_stock = df_stock[ns_parser.s_start_date :]

    # Daily
    if s_interval == "1440min":
        # The default doesn't exist for intradaily data
        ln_col_idx = [int(x) - 1 for x in list(type_candles)]
        # Check that the types given are not bigger than 4, as there are only 5 types (0-4)
        # pylint: disable=len-as-condition
        if len([i for i in ln_col_idx if i > 4]) > 0:
            print("An index bigger than 4 was given, which is wrong. Try again")
            return
        # Append last column of df to be filtered which corresponds to: 6. Volume
        ln_col_idx.append(5)
    # Intraday
    else:
        # The default doesn't exist for intradaily data
        if ns_parser.type == "a":
            ln_col_idx = [3]
        else:
            ln_col_idx = [int(x) - 1 for x in list(type_candles)]
        # Check that the types given are not bigger than 3, as there are only 4 types (0-3)
        # pylint: disable=len-as-condition
        if len([i for i in ln_col_idx if i > 3]) > 0:
            print("An index bigger than 3 was given, which is wrong. Try again")
            return
        # Append last column of df to be filtered which corresponds to: 5. Volume
        ln_col_idx.append(4)

    # Plot view of the stock
    plot_view_stock(df_stock.iloc[:, ln_col_idx], ns_parser.s_ticker)


def export(l_args, df_stock):
    parser = argparse.ArgumentParser(
        prog="export",
        description="Exports the historical data from this ticker to a file or stdout",
    )
    parser.add_argument(
        "-f",
        "--filename",
        type=str,
        dest="s_filename",
        default=stdout,
        help="Name of file to save the historical data exported (stdout if unspecified)",
    )
    parser.add_argument(
        "-F",
        "--format",
        dest="s_format",
        type=str,
        default="csv",
        help="Export historical data into following formats: csv, json, excel, clipboard",
    )
    try:
        ns_parser = parse_known_args_and_warn(parser, l_args)
    except SystemExit:
        print("")
        return

    if df_stock.empty:
        print("No data loaded yet to export.")
        return

    if ns_parser.s_format == "csv":
        df_stock.to_csv(ns_parser.s_filename)

    elif ns_parser.s_format == "json":
        df_stock.to_json(ns_parser.s_filename)

    elif ns_parser.s_format == "excel":
        df_stock.to_excel(ns_parser.s_filename)

    elif ns_parser.s_format == "clipboard":
        df_stock.to_clipboard()

    print("")
