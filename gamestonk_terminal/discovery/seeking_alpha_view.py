""" Seeking Alpha View """
__docformat__ = "numpy"

import argparse
from typing import List
import pandas as pd
from gamestonk_terminal.helper_funcs import (
    check_positive,
    parse_known_args_and_warn,
)

from gamestonk_terminal.discovery import seeking_alpha_model


def earnings_release_dates_view(other_args: List[str]):
    """Prints a data frame with earnings release dates

    Parameters
    ----------
    other_args : List[str]
        argparse other args - ["-p", "20", "-n", "5"]
    """

    parser = argparse.ArgumentParser(
        add_help=False,
        prog="up_earnings",
        description="""Upcoming earnings release dates. [Source: Seeking Alpha]""",
    )

    parser.add_argument(
        "-p",
        "--pages",
        action="store",
        dest="n_pages",
        type=check_positive,
        default=10,
        help="Number of pages to read upcoming earnings from in Seeking Alpha website.",
    )
    parser.add_argument(
        "-n",
        "--num",
        action="store",
        dest="n_num",
        type=check_positive,
        default=3,
        help="Number of upcoming earnings release dates to print",
    )

    ns_parser = parse_known_args_and_warn(parser, other_args)
    if not ns_parser:
        return

    df_earnings = seeking_alpha_model.get_next_earnings(ns_parser.n_pages)

    pd.set_option("display.max_colwidth", None)
    for n_days, earning_date in enumerate(df_earnings.index.unique()):
        if n_days > (ns_parser.n_num - 1):
            break

        print(f"Earning Release on {earning_date.date()}")
        print("----------------------------------------------")
        print(
            df_earnings[earning_date == df_earnings.index][
                ["Ticker", "Name"]
            ].to_string(index=False, header=False)
        )
        print("")


def latest_news_view(other_args: List[str]):
    """Prints the latest news article list

    Parameters
    ----------
    other_args : List[str]
        argparse other args - ["-n", "5"]
    """

    parser = argparse.ArgumentParser(
        add_help=False,
        prog="latest",
        description="""Latest news articles. [Source: Seeking Alpha]""",
    )

    parser.add_argument(
        "-n",
        "--num",
        action="store",
        dest="n_num",
        type=check_positive,
        default=10,
        help="number of latest articles being printed.",
    )

    ns_parser = parse_known_args_and_warn(parser, other_args)
    if not ns_parser:
        return

    articles = seeking_alpha_model.get_article_list(ns_parser.n_num)
    for idx, article in enumerate(articles):
        print(
            article["publishedAt"].replace("T", " ").replace("Z", ""),
            "-",
            article['id'],
            "-",
            article["title"],
        )
        print(article["url"])
        print("")

        if idx >= ns_parser.n_num - 1:
            break


def trending_news_view(other_args: List[str]):
    """Prints the trending news article list

    Parameters
    ----------
    other_args : List[str]
        argparse other args - ["-n", "5"]
    """

    parser = argparse.ArgumentParser(
        add_help=False,
        prog="trending",
        description="""Trending news articles. [Source: Seeking Alpha]""",
    )

    parser.add_argument(
        "-n",
        "--num",
        action="store",
        dest="n_num",
        type=check_positive,
        default=10,
        help="number of trending articles being printed.",
    )

    ns_parser = parse_known_args_and_warn(parser, other_args)
    if not ns_parser:
        return

    articles = seeking_alpha_model.get_trending_list(ns_parser.n_num)
    for idx, article in enumerate(articles):
        print(
            article["publishedAt"].replace("T", " ").replace("Z", ""),
            "-",
            article['id'],
            "-",
            article["title"],
        )
        print(article["url"])
        print("")

        if idx >= ns_parser.n_num - 1:
            break


def news_article_view(other_args: List[str]):
    """Prints a news article

    Parameters
    ----------
    other_args : List[str]
        argparse other args - ["-i", "3681944"]
    """

    parser = argparse.ArgumentParser(
        add_help=False,
        prog="up_article",
        description="""News article. [Source: Seeking Alpha]""",
    )

    parser.add_argument(
        "-i",
        "--id",
        action="store",
        dest="n_id",
        type=check_positive,
        default=-1,
        help="Article number found on Seeking Alpha website.",
    )

    ns_parser = parse_known_args_and_warn(parser, other_args)
    if not ns_parser:
        return
    if ns_parser.n_id == -1:
        return

    article = seeking_alpha_model.get_article_data(ns_parser.n_id)
    print(article['publishedAt'], " ", article['title'])
    print(article["url"])
    print("")
    print(article['content'])
