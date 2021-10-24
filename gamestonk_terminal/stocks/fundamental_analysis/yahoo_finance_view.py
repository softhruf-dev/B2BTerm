""" Yahoo Finance View """
__docformat__ = "numpy"

import webbrowser
from tabulate import tabulate

from gamestonk_terminal.stocks.fundamental_analysis import yahoo_finance_model
from gamestonk_terminal import feature_flags as gtff


def open_headquarters_map(ticker: str):
    """Headquarters location of the company

    Parameters
    ----------
    ticker : str
        Fundamental analysis ticker symbol
    """
    webbrowser.open(yahoo_finance_model.get_hq(ticker))
    print("")


def open_web(ticker: str):
    """Website of the company

    Parameters
    ----------
    ticker : str
        Fundamental analysis ticker symbol
    """
    webbrowser.open(yahoo_finance_model.get_website(ticker))
    print("")


def display_info(ticker: str):
    """Yahoo Finance ticker info

    Parameters
    ----------
    ticker : str
        Fundamental analysis ticker symbol
    """
    summary = ""
    df_info = yahoo_finance_model.get_info(ticker)
    if "Long business summary" in df_info.index:
        summary = df_info.loc["Long business summary"].values[0]
        df_info = df_info.drop(index=["Long business summary"])

    if gtff.USE_TABULATE_DF:
        print(tabulate(df_info, headers=[], showindex=True, tablefmt="fancy_grid"))

    else:
        print(df_info.to_string(header=False))

    if summary:
        print("Business Summary:")
        print(summary)

    print("")


def display_shareholders(ticker: str):
    """Yahoo Finance ticker shareholders

    Parameters
    ----------
    ticker : str
        Fundamental analysis ticker symbol
    """
    (
        df_major_holders,
        df_institutional_shareholders,
        df_mutualfund_shareholders,
    ) = yahoo_finance_model.get_shareholders(ticker)

    dfs = [df_major_holders, df_institutional_shareholders, df_mutualfund_shareholders]
    titles = ["Major Holders:\n", "Institutuinal Holders:\n", "Mutual Fund Holders:\n"]
    print("")
    for df, title in zip(dfs, titles):
        print(title)
        if gtff.USE_TABULATE_DF:
            print(
                tabulate(df, headers=df.columns, tablefmt="fancy_grid", showindex=False)
            )
        else:
            print(df.to_string(index=False))
        print("")


def display_sustainability(ticker: str):
    """Yahoo Finance ticker sustainability

    Parameters
    ----------
    other_args : List[str]
        argparse other args
    ticker : str
        Fundamental analysis ticker symbol
    """

    df_sustainability = yahoo_finance_model.get_sustainability(ticker)

    if df_sustainability.empty:
        print("No sustainability data found.")
        return

    if gtff.USE_TABULATE_DF:
        print(
            tabulate(
                df_sustainability,
                headers=[],
                tablefmt="fancy_grid",
                showindex=True,
            )
        )
    else:
        print(df_sustainability.to_sring(index=True))
    print("")


def display_calendar_earnings(ticker: str):
    """Yahoo Finance ticker calendar earnings

    Parameters
    ----------
    ticker : str
        Fundamental analysis ticker symbol
    """
    df_calendar = yahoo_finance_model.get_calendar_earnings(ticker).T
    if df_calendar.empty:
        print("No calendar events found.\n")
        return
    if gtff.USE_TABULATE_DF:
        print(
            tabulate(
                df_calendar,
                showindex=False,
                headers=df_calendar.columns,
                tablefmt="fancy_grid",
            )
        )
    else:
        print(df_calendar.to_string(index=False))
    print("")
