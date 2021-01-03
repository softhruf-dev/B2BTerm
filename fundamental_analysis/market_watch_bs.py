import argparse
import pandas as pd
from bs4 import BeautifulSoup
import requests

# ---------------------------------------------------- INCOME ----------------------------------------------------
def income(l_args, s_ticker):
    parser = argparse.ArgumentParser(prog='incom', 
                                     description="""Gives income statement the company. The following fields are expected: 
                                     Sales Growth, Cost of Goods Sold (COGS) incl. D&A, COGS Growth, COGS excluding D&A, 
                                     Depreciation & Amortization Expense, Depreciation, Amortization of Intangibles, Gross Income, 
                                     Gross Income Growth, Gross Profit Margin, SG&A Expense, SGA Growth, Research & Development, 
                                     Other SG&A, Other Operating Expense, Unusual Expense, EBIT after Unusual Expense, 
                                     Non Operating Income/Expense, Non-Operating Interest Income, Equity in Affiliates (Pretax), 
                                     Interest Expense, Interest Expense Growth, Gross Interest Expense, Interest Capitalized, 
                                     Pretax Income, Pretax Income Growth, Pretax Margin, Income Tax, Income Tax - Current Domestic, 
                                     Income Tax - Current Foreign, Income Tax - Deferred Domestic, Income Tax - Deferred Foreign, 
                                     Income Tax Credits, Equity in Affiliates, Other After Tax Income (Expense), Consolidated Net Income, 
                                     Minority Interest Expense, Net Income Growth, Net Margin Growth, Extraordinaries & Discontinued Operations, 
                                     Extra Items & Gain/Loss Sale Of Assets, Cumulative Effect - Accounting Chg, Discontinued Operations, 
                                     Net Income After Extraordinaries, Preferred Dividends, Net Income Available to Common, EPS (Basic), 
                                     EPS (Basic) Growth, Basic Shares Outstanding, EPS (Diluted), EPS (Diluted) Growth, Diluted Shares Outstanding, 
                                     EBITDA, EBITDA Growth, EBITDA Margin, Sales/Revenue, and Net Income. [Source: Market Watch BS]""")
    
    parser.add_argument('-q', "--quarter", action="store_true", default=False, dest="b_quarter", help='Quarter fundamental data')

    try:
        (ns_parser, l_unknown_args) = parser.parse_known_args(l_args)

        if l_unknown_args:
            print(f"The following args couldn't be interpreted: {l_unknown_args}")

        if ns_parser.b_quarter:
            url_financials = f"https://www.marketwatch.com/investing/stock/{s_ticker}/financials/income/quarter"
        else:
            url_financials = f"https://www.marketwatch.com/investing/stock/{s_ticker}/financials/income"
            
        text_soup_financials = BeautifulSoup(requests.get(url_financials).text, "lxml")

        # Define financials columns
        a_financials_header = list()
        for financials_header in text_soup_financials.findAll('th',  {'class': 'overflow__heading'}):
            a_financials_header.append(financials_header.text.strip('\n').split('\n')[0])
        df_financials = pd.DataFrame(columns=a_financials_header[0:-1])

        # Add financials values
        soup_financials = text_soup_financials.findAll('tr', {'class': 'table__row '})
        soup_financials += text_soup_financials.findAll('tr', {'class': 'table__row is-highlighted'})
        for financials_info in soup_financials:
            a_financials_info = financials_info.text.split('\n')
            l_financials = [a_financials_info[2]] 
            l_financials.extend(a_financials_info[5:-2])
            # Append data values to financials
            df_financials.loc[len(df_financials.index)] = l_financials

        print(df_financials.to_string(index=False))
        print("")

    except:
        print("ERROR!\n")
        return


# ---------------------------------------------------- ASSETS ----------------------------------------------------
def assets(l_args, s_ticker):
    parser = argparse.ArgumentParser(prog='assets', 
                                     description="""Gives income statement the company. The following fields are expected: 
                                     Cash & Short Term Investments, Cash & Short Term Investments Growth, Cash Only, 
                                     Short-Term Investments, Cash & ST Investments / Total Assets, Total Accounts Receivable, 
                                     Total Accounts Receivable Growth, Accounts Receivables, Net, Accounts Receivables, Gross, 
                                     Bad Debt/Doubtful Accounts, Other Receivable, Accounts Receivable Turnover, Inventories, 
                                     Finished Goods, Work in Progress, Raw Materials, Progress Payments & Other, Other Current Assets, 
                                     Miscellaneous Current Assets, Net Property, Plant & Equipment, Property, Plant & Equipment - Gross, 
                                     Buildings, Land & Improvements, Computer Software and Equipment, Other Property, Plant & Equipment, 
                                     Accumulated Depreciation, Total Investments and Advances, Other Long-Term Investments, 
                                     Long-Term Note Receivables, Intangible Assets, Net Goodwill, Net Other Intangibles, Other Assets
                                     [Source: Market Watch BS]""")
    
    parser.add_argument('-q', "--quarter", action="store_true", default=False, dest="b_quarter", help='Quarter fundamental data')

    try:
        (ns_parser, l_unknown_args) = parser.parse_known_args(l_args)

        if l_unknown_args:
            print(f"The following args couldn't be interpreted: {l_unknown_args}")

        if ns_parser.b_quarter:
            url_financials = f"https://www.marketwatch.com/investing/stock/{s_ticker}/financials/balance-sheet/quarter"
        else:
            url_financials = f"https://www.marketwatch.com/investing/stock/{s_ticker}/financials/balance-sheet"
            
        text_soup_financials = BeautifulSoup(requests.get(url_financials).text, "lxml")

        # Define financials columns
        a_financials_header = list()
        for financials_header in text_soup_financials.findAll('th',  {'class': 'overflow__heading'}):
            a_financials_header.append(financials_header.text.strip('\n').split('\n')[0])
        s_header_end_trend = ("5-year trend", "5- qtr trend")[ns_parser.b_quarter]
        df_financials = pd.DataFrame(columns=a_financials_header[0:a_financials_header.index(s_header_end_trend)])

        # Add financials values
        soup_financials = text_soup_financials.findAll('tr', {'class': 'table__row '})
        soup_financials += text_soup_financials.findAll('tr', {'class': 'table__row is-highlighted'})
        for financials_info in soup_financials:
            a_financials_info = financials_info.text.split('\n')
            l_financials = [a_financials_info[2]] 
            l_financials.extend(a_financials_info[5:-2])
            # Append data values to financials
            df_financials.loc[len(df_financials.index)] = l_financials

        # Set item name as index
        df_financials = df_financials.set_index('Item')

        print(df_financials.iloc[:33].to_string())
        print("")

    except:
        print("ERROR!\n")
        return
