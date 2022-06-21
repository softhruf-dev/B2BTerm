```text
usage: ln -n NAME [NAME ...] [-s {sa,fd}] [-l LIMIT] [-h] [--export {csv,json,xlsx}]
```

Search for an ETF by name, using either FinanceDatabase or Stockanalysis.com as the source.

````
optional arguments:
  -n NAME [NAME ...], --name NAME [NAME ...]
                        Name to look for ETFs (default: None)
  -h, --help            show this help message (default: False)
  --export EXPORT       Export raw data into csv, json, xlsx (default: )
  -l LIMIT, --limit LIMIT
                        Number of entries to show in data. (default: 5)
  --source {sa,fd}      Data source to select from (default: None)
````

Sample output:

```
2022 Jan 18, 23:49 (✨) /etf/ $ ln energy -l 10
╒══════╤═══════════════════════════════════════════════════════╤═══════════════════════════════════╤════════════════════════════╤════════════════════╕
│      │ Name                                                  │ Family                            │ Category                   │   Total Assets [M] │
╞══════╪═══════════════════════════════════════════════════════╪═══════════════════════════════════╪════════════════════════════╪════════════════════╡
│ XLE  │ Energy Select Sector SPDR Fund                        │ SPDR State Street Global Advisors │ Equity Energy              │           23081.07 │
├──────┼───────────────────────────────────────────────────────┼───────────────────────────────────┼────────────────────────────┼────────────────────┤
│ VDE  │ Vanguard Energy Index Fund ETF Shares                 │ Vanguard                          │ Equity Energy              │            5883.56 │
├──────┼───────────────────────────────────────────────────────┼───────────────────────────────────┼────────────────────────────┼────────────────────┤
│ ICLN │ iShares Global Clean Energy ETF                       │ iShares                           │ Miscellaneous Sector       │            5811.92 │
├──────┼───────────────────────────────────────────────────────┼───────────────────────────────────┼────────────────────────────┼────────────────────┤
│ QCLN │ First Trust NASDAQ Clean Edge Green Energy Index Fund │ First Trust                       │ Miscellaneous Sector       │            2680.65 │
├──────┼───────────────────────────────────────────────────────┼───────────────────────────────────┼────────────────────────────┼────────────────────┤
│ PBW  │ Invesco WilderHill Clean Energy ETF                   │ Invesco                           │ Miscellaneous Sector       │            2200.06 │
├──────┼───────────────────────────────────────────────────────┼───────────────────────────────────┼────────────────────────────┼────────────────────┤
│ EMLP │ First Trust North American Energy Infrastructure Fund │ First Trust                       │ Energy Limited Partnership │            1858.28 │
├──────┼───────────────────────────────────────────────────────┼───────────────────────────────────┼────────────────────────────┼────────────────────┤
│ IXC  │ iShares Global Energy ETF                             │ iShares                           │ Equity Energy              │            1312.18 │
├──────┼───────────────────────────────────────────────────────┼───────────────────────────────────┼────────────────────────────┼────────────────────┤
│ ACES │ ALPS Clean Energy ETF                                 │ ALPS                              │ Equity Energy              │             970.75 │
├──────┼───────────────────────────────────────────────────────┼───────────────────────────────────┼────────────────────────────┼────────────────────┤
│ FENY │ Fidelity MSCI Energy Index ETF                        │ Fidelity Investments              │ Equity Energy              │             889.72 │
├──────┼───────────────────────────────────────────────────────┼───────────────────────────────────┼────────────────────────────┼────────────────────┤
│ MLPX │ Global X MLP & Energy Infrastructure ETF              │ Global X Funds                    │ Energy Limited Partnership │             714.83 │
╘══════╧═══════════════════════════════════════════════════════╧═══════════════════════════════════╧════════════════════════════╧════════════════════╛ 
```
