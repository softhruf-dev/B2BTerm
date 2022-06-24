---
title: Introduction to Funds
keywords: "funds, mutual funds, fund, basket, retail, institutional"
excerpt: "The Introduction to Funds explains how to use the 
menu and provides a brief description of its sub-menus"
geekdocCollapseSection: true
---
The Funds menu enables you to lookup any fund based on the selected <a href="https://openbb-finance.github.io/OpenBBTerminal/terminal/funds/country/" target="_blank">country</a> by using
<a href="https://openbb-finance.github.io/OpenBBTerminal/terminal/funds/overview/" target="_blank">overview</a> and <a href="https://openbb-finance.github.io/OpenBBTerminal/terminal/funds/search/" target="_blank">search</a>. Then, there is the ability to load in the symbol with <a href="https://openbb-finance.github.io/OpenBBTerminal/terminal/funds/load/" target="_blank">load</a>.
This opens up options to look into <a href="https://openbb-finance.github.io/OpenBBTerminal/terminal/funds/info/" target="_blank">fund information</a>, <a href="https://openbb-finance.github.io/OpenBBTerminal/terminal/funds/sector/" target="_blank">sector holdings</a>  and <a href="https://openbb-finance.github.io/OpenBBTerminal/terminal/funds/equity/" target="_blank">equity holdings</a>
as well as <a href="https://openbb-finance.github.io/OpenBBTerminal/terminal/funds/plot/" target="_blank">plot</a> the historical data.

## How to use

The Funds menu is called upon by typing `funds` which opens the following menu:

![Funds Menu](https://user-images.githubusercontent.com/46355364/174990788-3b432068-f303-4548-b9b5-0cb158e62628.png)

You have the ability to look up any fund (<a href="https://openbb-finance.github.io/OpenBBTerminal/terminal/funds/overview/" target="_blank">overview</a> or <a href="https://openbb-finance.github.io/OpenBBTerminal/terminal/funds/search/" target="_blank">search</a>). With the example below, the `search` command is used that searches the name and description of the fund. Then the search query is entered which is `total market`. Lastly, the `-l` argument is included which refers to `limit` and is maxed to `10` funds.
````
2022 Jun 22, 04:20 (🦋) /funds/ $ search total market -l 10

                                                        Mutual Funds with name matching total market
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ name                                                                  ┃ symbol     ┃ issuer                       ┃ isin         ┃ asset_class ┃ currency ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ State Street U.s. Total Market Index Non-lending Series Fund Class A  │ 0P0000RT44 │ State Street Global Advisors │ US85744U4022 │ equity      │ USD      │
├───────────────────────────────────────────────────────────────────────┼────────────┼──────────────────────────────┼──────────────┼─────────────┼──────────┤
│ Nh Unique College Investing Plan Total Market Index Portfolio         │ 0P0000O6ZV │ Fidelity Investments         │ US37N9946965 │ equity      │ USD      │
├───────────────────────────────────────────────────────────────────────┼────────────┼──────────────────────────────┼──────────────┼─────────────┼──────────┤
│ Ma U.fund College Investing Plan Spartan Total Market Index Portfolio │ 0P0000O6ML │ Fidelity Investments         │ US10W99R2702 │ equity      │ USD      │
├───────────────────────────────────────────────────────────────────────┼────────────┼──────────────────────────────┼──────────────┼─────────────┼──────────┤
│ Fidelity Zero Total Market Index Fund                                 │ FZROX      │ Fidelity Investments         │ US31635T7081 │ equity      │ USD      │
├───────────────────────────────────────────────────────────────────────┼────────────┼──────────────────────────────┼──────────────┼─────────────┼──────────┤
│ Fidelity Total Market Index Fund Class F                              │ FFSMX      │ Fidelity Investments         │ US3159117767 │ equity      │ USD      │
├───────────────────────────────────────────────────────────────────────┼────────────┼──────────────────────────────┼──────────────┼─────────────┼──────────┤
│ Fidelity Total Market Index Fund                                      │ FSKAX      │ Fidelity Investments         │ US3159116934 │ equity      │ USD      │
├───────────────────────────────────────────────────────────────────────┼────────────┼──────────────────────────────┼──────────────┼─────────────┼──────────┤
│ De College Investment Plan Spartan Total Market Index Portfolio       │ 0P0000O6T1 │ Fidelity Investments         │ US37Q99B3259 │ equity      │ USD      │
├───────────────────────────────────────────────────────────────────────┼────────────┼──────────────────────────────┼──────────────┼─────────────┼──────────┤
│ Blackrock Advantage U.s. Total Market Fund, Inc.investor C Shares     │ MCSPX      │ BlackRock                    │ US09252L3078 │ equity      │ USD      │
├───────────────────────────────────────────────────────────────────────┼────────────┼──────────────────────────────┼──────────────┼─────────────┼──────────┤
│ Blackrock Advantage U.s. Total Market Fund, Inc.investor A Shares     │ MDSPX      │ BlackRock                    │ US09252L1098 │ equity      │ USD      │
├───────────────────────────────────────────────────────────────────────┼────────────┼──────────────────────────────┼──────────────┼─────────────┼──────────┤
│ Blackrock Advantage U.s. Total Market Fund, Inc.institutional Shares  │ MASPX      │ BlackRock                    │ US09252L5057 │ equity      │ USD      │
└───────────────────────────────────────────────────────────────────────┴────────────┴──────────────────────────────┴──────────────┴─────────────┴──────────┘
````

This results in a selection of funds with their name, symbol, issuer, isin, asset class and currency. With this information, you can load in one of the symbols into the menu.
This can be done with <a href="https://openbb-finance.github.io/OpenBBTerminal/terminal/funds/load" target="_blank">load</a>.
See the following example:

````
2022 Jun 22, 04:30 (🦋) /funds/ $ load MDSPX
Name: Blackrock Advantage U.S. Total Market Fund, Inc.Investor A Shares found for MDSPX in country: United States.
````
To then view the stock chart, you can call <a href="https://openbb-finance.github.io/OpenBBTerminal/terminal/funds/plot/" target="_blank">plot</a>
which shows a chart for the defined period (by default set to a year by `load`):

![Plot](https://user-images.githubusercontent.com/46355364/174990848-8f0be3b3-945b-4e4d-801a-5a6a036b62c0.png)

By calling `?` or `help` the Funds menu re-appears. Here you can see that multiple commands have turned blue. Because of loading 
a symbol, these commands can now be used in combination with the chosen symbol as seen above.

![Funds Menu with Fund Loaded](https://user-images.githubusercontent.com/46355364/174990913-0a4e69bd-30d6-4a7f-adda-b921cfb21076.png)

For example, the Fund's general statistics can now be depicted with the following:
````
2022 Jun 22, 04:34 (🦋) /funds/ $ info

    Blackrock Advantage U.S. Total Market Fund, Inc.Investor A Shares Information
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Info           ┃ Value                                                             ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Fund Name      │ blackrock advantage u.s. total market fund, inc.investor a shares │
├────────────────┼───────────────────────────────────────────────────────────────────┤
│ 1-Year Change  │ - 25.21%                                                          │
├────────────────┼───────────────────────────────────────────────────────────────────┤
│ TTM Yield      │ 0.98%                                                             │
├────────────────┼───────────────────────────────────────────────────────────────────┤
│ ROE            │ 14.91%                                                            │
├────────────────┼───────────────────────────────────────────────────────────────────┤
│ Turnover       │ 71%                                                               │
├────────────────┼───────────────────────────────────────────────────────────────────┤
│ ROA            │ 4.94%                                                             │
├────────────────┼───────────────────────────────────────────────────────────────────┤
│ Inception Date │ 34628.00                                                          │
├────────────────┼───────────────────────────────────────────────────────────────────┤
│ Total Assets   │ 181230000.00                                                      │
├────────────────┼───────────────────────────────────────────────────────────────────┤
│ Expenses       │ 0.73%                                                             │
├────────────────┼───────────────────────────────────────────────────────────────────┤
│ Market Cap     │ 6380000000.00                                                     │
└────────────────┴───────────────────────────────────────────────────────────────────┘
````

## Examples

If we want to learn more about a bond fund, we can do the following, starting from the `funds` menu and using
the `search` command where we specify with `-l` we wish to see `15` funds max.

```
2022 Jun 22, 04:40 (🦋) /funds/ $ search bond fund -l 15

                                              Mutual Funds with name matching bond fund
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ name                                                       ┃ symbol     ┃ issuer           ┃ isin         ┃ asset_class ┃ currency ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ Wilmington Short-term Bond Fund Institutional Class        │ MVSTX      │ Wilmington Funds │ US97181C5976 │ bond        │ USD      │
├────────────────────────────────────────────────────────────┼────────────┼──────────────────┼──────────────┼─────────────┼──────────┤
│ Wilmington Municipal Bond Fund Class Institutional         │ WTAIX      │ Wilmington Funds │ US97181C4565 │ equity      │ USD      │
├────────────────────────────────────────────────────────────┼────────────┼──────────────────┼──────────────┼─────────────┼──────────┤
│ Wilmington Intermediate-term Bond Fund Institutional Class │ ARIFX      │ Wilmington Funds │ US97181C8459 │ bond        │ USD      │
├────────────────────────────────────────────────────────────┼────────────┼──────────────────┼──────────────┼─────────────┼──────────┤
│ Wilmington Broad Market Bond Fund Institutional Class      │ ARKIX      │ Wilmington Funds │ US97181C8111 │ bond        │ USD      │
├────────────────────────────────────────────────────────────┼────────────┼──────────────────┼──────────────┼─────────────┼──────────┤
│ Western Asset Short-term Bond Fund Class Is                │ LWSTX      │ Legg Mason       │ US52468A7312 │ bond        │ USD      │
├────────────────────────────────────────────────────────────┼────────────┼──────────────────┼──────────────┼─────────────┼──────────┤
│ Western Asset Intermediate Bond Fund Class Is              │ WABSX      │ Legg Mason       │ US9576636107 │ bond        │ USD      │
├────────────────────────────────────────────────────────────┼────────────┼──────────────────┼──────────────┼─────────────┼──────────┤
│ Western Asset Intermediate Bond Fund Class I               │ WATIX      │ Legg Mason       │ US9576637014 │ bond        │ USD      │
├────────────────────────────────────────────────────────────┼────────────┼──────────────────┼──────────────┼─────────────┼──────────┤
│ Western Asset Inflation Indexed Plus Bond Fund Class Is    │ WAFSX      │ Legg Mason       │ US9576635455 │ bond        │ USD      │
├────────────────────────────────────────────────────────────┼────────────┼──────────────────┼──────────────┼─────────────┼──────────┤
│ Western Asset Global High Yield Bond Fund Class Is         │ LWGSX      │ Legg Mason       │ US52468A7239 │ bond        │ USD      │
├────────────────────────────────────────────────────────────┼────────────┼──────────────────┼──────────────┼─────────────┼──────────┤
│ Western Asset Global High Yield Bond Fund Class A          │ SAHYX      │ Legg Mason       │ US52469F4651 │ bond        │ USD      │
├────────────────────────────────────────────────────────────┼────────────┼──────────────────┼──────────────┼─────────────┼──────────┤
│ Western Asset Corporate Bond Fund Class P                  │ 0P0000JCKF │ Legg Mason       │ US52469L6609 │ bond        │ USD      │
├────────────────────────────────────────────────────────────┼────────────┼──────────────────┼──────────────┼─────────────┼──────────┤
│ Western Asset Corporate Bond Fund Class I                  │ 0P00002OJN │ Legg Mason       │ US52469F2754 │ bond        │ USD      │
├────────────────────────────────────────────────────────────┼────────────┼──────────────────┼──────────────┼─────────────┼──────────┤
│ Western Asset Corporate Bond Fund Class C1                 │ 0P00002Q4W │ Legg Mason       │ US52469F2838 │ bond        │ USD      │
├────────────────────────────────────────────────────────────┼────────────┼──────────────────┼──────────────┼─────────────┼──────────┤
│ Western Asset Corporate Bond Fund Class A                  │ SIGAX      │ Legg Mason       │ US52469F3174 │ bond        │ USD      │
├────────────────────────────────────────────────────────────┼────────────┼──────────────────┼──────────────┼─────────────┼──────────┤
│ Western Asset Core Bond Fund Class R                       │ 0P0000VORL │ Legg Mason       │ US9576634797 │ bond        │ USD      │
└────────────────────────────────────────────────────────────┴────────────┴──────────────────┴──────────────┴─────────────┴──────────┘
```

Here, we decide to grab a corporate bond fund, Western Asset Corporate Bond Fund Class A (SIGAX) by loading in the data with <a href="https://openbb-finance.github.io/OpenBBTerminal/terminal/funds/load" target="_blank">load</a>.
Also, a larger period is chosen by using `-s` as shown in the documentation:

```` 
2022 Jun 22, 04:58 (🦋) /funds/ $ load SIGAX -s 2015-01-01
Name: Western Asset Corporate Bond Fund Class A found for SIGAX in country: United States.
````

We can now plot the corresponding funds chart with <a href="https://openbb-finance.github.io/OpenBBTerminal/terminal/funds/plot/" target="_blank">plot</a> which shows
the company's historical data from `2015-01-01` until the current date.

```
2022 Jun 22, 04:58 (🦋) /funds/ $ plot
```

![Plot #2](https://user-images.githubusercontent.com/46355364/174990983-d052370c-825a-480e-adaf-239e75b26675.png)

Now we can go ahead and explore more about the fund by running <a href="https://openbb-finance.github.io/OpenBBTerminal/terminal/funds/info/" target="_blank">info</a>.
This provides some general statistics about the fund.
```
2022 Jun 22, 05:00 (🦋) /funds/ $ info

    Western Asset Corporate Bond Fund Class A Information
┏━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Info           ┃ Value                                     ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Fund Name      │ western asset corporate bond fund class a │
├────────────────┼───────────────────────────────────────────┤
│ 1-Year Change  │ - 18.06%                                  │
├────────────────┼───────────────────────────────────────────┤
│ TTM Yield      │ 2.76%                                     │
├────────────────┼───────────────────────────────────────────┤
│ ROE            │ 8.87%                                     │
├────────────────┼───────────────────────────────────────────┤
│ Turnover       │ 63%                                       │
├────────────────┼───────────────────────────────────────────┤
│ ROA            │ 6.18%                                     │
├────────────────┼───────────────────────────────────────────┤
│ Inception Date │ 33914.00                                  │
├────────────────┼───────────────────────────────────────────┤
│ Total Assets   │ 268590000.00                              │
├────────────────┼───────────────────────────────────────────┤
│ Expenses       │ 0.87%                                     │
├────────────────┼───────────────────────────────────────────┤
│ Market Cap     │ 6070000000.00                             │
└────────────────┴───────────────────────────────────────────┘
```
