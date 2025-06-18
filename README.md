# TaxRedistributionPaper
Code repository for Coleman-Weisbach paper "How Much Does U.S. Fiscal System Redistribute?"

## Data

- AutenSplinter-IncomeIneq_2024.xlsx
  - Spreadsheet with detailed data from Auten, Gerald, and David Splinter. 2024. “Income Inequality in the United States: Using Tax Data to Measure Long-Term Trends.” Journal of Political Economy 132 (7): 2179–2227. https://doi.org/10.1086/728741.  Auten & Splinter (2024)
  - Downloaded September 2024 from http://davidsplinter.com/AutenSplinter-IncomeIneq.xlsx
- PSZ2022AppendixTablesII(Distrib).xlsx
  - Spreadsheet with detailed data from Piketty, Thomas, Emmanuel Saez, and Gabriel Zucman. 2018. “Distributional National Accounts: Methods and Estimates for the United States.” Quarterly Journal of Economics 133 (2): 553–609. https://doi.org/10.1093/qje/qjx043.
  - Downloaded August 2023 from https://gabriel-zucman.eu/usdina/ (listed as 'Tables II: distributional series (.xlsx)')
- households_ranked_by_inc_before_trans_tax_table_03_average_household_income_1979_2019.csv
- households_ranked_by_market_inc_table_03_average_household_income_1979_2019.csv
  - CBO data, downloaded November 2022 from https://www.cbo.gov/publication/58353 entry 'Additional Data for Researchers (zip file)' 
- 58353-supplemental-data.xlsx
  - CBO data, downloaded November 2023 from https://www.cbo.gov/publication/58353 entry  'Supplemental Data'

## Code

- Python code to produce tables and graphs
- Run from the directory set to the same directory as the code & data
  - Table1.py: reads data from PSZ and AS spreadsheets, calculates and prints Table 1
  - Figure1.py: reads data from PSZ spreadsheet, produces Figure 1
  - Figure3&4.py: reads data from PSZ and AS spreadsheets, CBO .csv files, and produces Figures 3 & 4
  - Figure3_alt2.py: reads data from PSZ and AS spreadsheets, CBO .csv files, and produces alternate versions of Figure 3 (Figures A1 & A2) that compares PSZ vs AS for Before-vs-After-Tax income (not consistent rankings) and for PSZ Factor Income and Pre-Tax ('hybrid') Income
  - Figure5.py: reads data from PSZ, AS, and CBO spreadsheets, and produces Figures 5, A3, A4
  - Figure6.py: reads data from PSZ and AS spreadsheets, and produces Figures 6, 7, A5
  - Figure8.py: reads data from AS spreadsheet, and produces Figure 8





