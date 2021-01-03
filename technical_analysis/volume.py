import argparse
import pandas_ta as ta
from stock_market_helper_funcs import *
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# ------------------------------------------------------- AD -------------------------------------------------------
def ad(l_args, s_ticker, s_interval, df_stock):
    parser = argparse.ArgumentParser(prog='ad', 
                                     description=""" The Accumulation/Distribution Line is similar to the On Balance 
                                     Volume (OBV), which sums the volume times +1/-1 based on whether the close is 
                                     higher than the previous close. The Accumulation/Distribution indicator, however 
                                     multiplies the volume by the close location value (CLV). The CLV is based on the 
                                     movement of the issue within a single bar and can be +1, -1 or zero. \n \n 
                                     The Accumulation/Distribution Line is interpreted by looking for a divergence in 
                                     the direction of the indicator relative to price. If the Accumulation/Distribution 
                                     Line is trending upward it indicates that the price may follow. Also, if the 
                                     Accumulation/Distribution Line becomes flat while the price is still rising (or falling) 
                                     then it signals an impending flattening of the price.""")

    parser.add_argument('-o', "--offset", action="store", dest="n_offset", type=check_positive, default=0, help='offset')
    parser.add_argument('--open', action="store_true", default=False, dest="b_use_open", help='uses open value of stock')

    try:
        (ns_parser, l_unknown_args) = parser.parse_known_args(l_args)

        if l_unknown_args:
            print(f"The following args couldn't be interpreted: {l_unknown_args}")

        # Daily
        if s_interval == "1440min":
            # Use open stock values
            if ns_parser.b_use_open:
                df_ta = ta.ad(high=df_stock['2. high'], low=df_stock['3. low'], close=df_stock['5. adjusted close'], 
                              volume=df_stock['6. volume'], offset=ns_parser.n_offset, open_=df_stock['1. open']).dropna()
            # Do not use open stock values
            else:
                df_ta = ta.ad(high=df_stock['2. high'], low=df_stock['3. low'], close=df_stock['5. adjusted close'], 
                              volume=df_stock['6. volume'], offset=ns_parser.n_offset).dropna()

            plot_stock_and_ta(df_stock['5. adjusted close'], s_ticker, df_ta, "AD")
        # Intraday 
        else:
            # Use open stock values
            if ns_parser.b_use_open:
                df_ta = ta.ad(high=df_stock['2. high'], low=df_stock['3. low'], close=df_stock['4. close'], 
                              volume=df_stock['5. volume'], offset=ns_parser.n_offset, open_=df_stock['1. open']).dropna()
            # Do not use open stock values
            else:
                df_ta = ta.ad(high=df_stock['2. high'], low=df_stock['3. low'], close=df_stock['4. close'], 
                              volume=df_stock['5. volume'], offset=ns_parser.n_offset).dropna()
        
            plot_stock_and_ta(df_stock['4. close'], s_ticker, df_ta, "AD")

    except:
        print("ERROR!\n")
        return
    

# ------------------------------------------------------- OBV -------------------------------------------------------
def obv(l_args, s_ticker, s_interval, df_stock):
    parser = argparse.ArgumentParser(prog='obv', 
                                     description=""" The On Balance Volume (OBV) is a cumulative total of the up and 
                                     down volume. When the close is higher than the previous close, the volume is added 
                                     to the running total, and when the close is lower than the previous close, the volume 
                                     is subtracted from the running total. \n \n To interpret the OBV, look for the OBV 
                                     to move with the price or precede price moves. If the price moves before the OBV, 
                                     then it is a non-confirmed move. A series of rising peaks, or falling troughs, in the 
                                     OBV indicates a strong trend. If the OBV is flat, then the market is not trending. """)

    parser.add_argument('-o', "--offset", action="store", dest="n_offset", type=check_positive, default=0, help='offset')

    try:
        (ns_parser, l_unknown_args) = parser.parse_known_args(l_args)

        if l_unknown_args:
            print(f"The following args couldn't be interpreted: {l_unknown_args}")

        # Daily
        if s_interval == "1440min":
            df_ta = ta.obv(close=df_stock['5. adjusted close'], volume=df_stock['6. volume'], offset=ns_parser.n_offset).dropna()
            plot_stock_and_ta(df_stock['5. adjusted close'], s_ticker, df_ta, "OBV")
        # Intraday 
        else:
            df_ta = ta.obv(close=df_stock['4. close'], volume=df_stock['5. volume'], offset=ns_parser.n_offset).dropna()
            plot_stock_and_ta(df_stock['4. close'], s_ticker, df_ta, "OBV")

    except:
        print("ERROR!\n")
        return
    