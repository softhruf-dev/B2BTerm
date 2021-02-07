import argparse
import requests
import pandas as pd

# -------------------------------------------------------------------------------------------------------------------
def sentiment(l_args, s_ticker):
    parser = argparse.ArgumentParser(prog='sentiment', 
                                     description="""Gather a stock sentiment based on last 30 messages on the board.
                                     Also prints the watchlist_count [stocktwits] """)

    parser.add_argument('-t', "--ticker", action="store", dest="s_ticker", type=str, default=s_ticker, help='Ticker to gather sentiment')

    try:
        (ns_parser, l_unknown_args) = parser.parse_known_args(l_args)

        if l_unknown_args:
            print(f"The following args couldn't be interpreted: {l_unknown_args}\n")
            return

        result = requests.get(f"https://api.stocktwits.com/api/2/streams/symbol/{ns_parser.s_ticker}.json")
        if result.status_code == 200:
            print(f"Watchlist count: {result.json()['symbol']['watchlist_count']}")
            n_cases = 0
            n_bull = 0
            n_bear = 0
            for message in result.json()['messages']:
                if (message['entities']['sentiment']):
                    n_cases += 1
                    n_bull += (message['entities']['sentiment']['basic'] == 'Bullish')
                    n_bear += (message['entities']['sentiment']['basic'] == 'Bearish')

            if n_cases > 0:
                print(f"\nOver {n_cases} sentiment messages:")
                print(f"Bullish {round(100*n_bull/n_cases, 2)}%")
                print(f"Bearish {round(100*n_bear/n_cases, 2)}%")
        else:
            print("Invalid symbol")
    
        print("")

    except:
        print("")

