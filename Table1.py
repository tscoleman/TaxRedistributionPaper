#############################################
# Reads data from Auten & Splinter and      #
# Piketty, Saez, Zuchman, to calculate      #
# growth in per-capita income. For PSZ it is#
# from tabs TD5, TD7, 8, 9 and tabs TC5, 7  #
# 8, 9. For AS a little more complicate     #
# because need to calculate per-capita and  #
# real                                      #
#############################################


#%% Set up file names

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

pd.set_option('display.float_format', lambda x: '%.5f' % x)

dir_name = "/Users/tcoleman/tom/Economics/Harris/research/IncomeInequality/AS_PSZdata/"
dir_name = ''
file_pathPSZ = dir_name + "PSZ2022AppendixTablesII(Distrib).xlsx"
file_pathAS = dir_name + "AutenSplinter-IncomeIneq_2024.xlsx"

#%% Populate PSZ dataframes 

# Dictionary of dataframes holding the input data
dfdict = dict()

# Define dataframe which will be our table
x1 = {'Name': ['PSZ Fiscal Income per Return','PSZ Fiscal Income per adult','PSZ Pre-Tax Income','AS Pre-Tax Income'],
	'All':[1.,2.,3.,4.],
	'Bottom 50%': [4.,5.,6.,7.],
	'Middle 40%': [7.,8.,9.,10.],
	'Top 10%':[10.,11.,12.,13.]}
table1 = pd.DataFrame(x1)
table1.set_index('Name',inplace=True)

# Define years to use
years = [1979,2014]
# Define quantiles to use (columns)
quantiles = list(table1.columns)
# Names for rows 
names = list(table1.index.values)

# PSZ Fiscal Income by tax unit
tabledf = pd.read_excel(file_pathPSZ, sheet_name="TD3", skiprows=6)
tabledf.iloc[1, 0] = "Year"
tabledf.columns = tabledf.iloc[1]
tabledf = tabledf.drop([0,1]).apply(pd.to_numeric, errors='coerce')
tabledf.set_index('Year',inplace=True,drop=False)
tabledf.rename({'bottom 50%':'Bottom 50%'}, axis='columns',inplace=True)  # Bad name in spreadsheet

dfdict[names[0]] = tabledf

# PSZ Fiscal Income by adult
sheetlist = ['TD5','TD7','TD8','TD9']
for i,sheet in enumerate(sheetlist):
    tabledf = pd.read_excel(file_pathPSZ, sheet_name=sheet, skiprows=6)
    tabledf.iloc[0, 0] = "Year"
    tabledf.columns = tabledf.iloc[0]
    tabledf = tabledf.drop(0).apply(pd.to_numeric, errors='coerce')
    tabledf.set_index('Year',inplace=True,drop=False)
    if (i == 0):
        PSZ_comp = tabledf.iloc[:,0:2].copy()
        PSZ_comp.rename({'eqaul-split individual':'All'}, axis='columns',inplace=True)  # Bad name in spreadsheet
        PSZ_comp.rename({'Individuals':'All'}, axis='columns',inplace=True)  # Set name
    else:
        PSZ_comp[quantiles[i]] = tabledf.iloc[:,1].copy()
dfdict[names[1]] = PSZ_comp

# PSZ Pre-tax Income by adult
sheetlist = ['TB5','TB7','TB8','TB9']
for i,sheet in enumerate(sheetlist):
    tabledf = pd.read_excel(file_pathPSZ, sheet_name=sheet, skiprows=6)
    tabledf.iloc[0, 0] = "Year"
    tabledf.columns = tabledf.iloc[0]
    tabledf = tabledf.drop(0).apply(pd.to_numeric, errors='coerce')
    tabledf.set_index('Year',inplace=True,drop=False)
    if (i == 0):
        PSZ_comp = tabledf.iloc[:,0:2].copy()
        PSZ_comp.rename({'eqaul-split individual':'All'}, axis='columns',inplace=True)  # Bad name in spreadsheet
        PSZ_comp.rename({'Individuals':'All'}, axis='columns',inplace=True)  # Set name
    else:
        PSZ_comp[quantiles[i]] = tabledf.iloc[:,1].copy()
dfdict[names[2]] = PSZ_comp


#%% Populate Auten & Splinter dataframe

as_C1 = pd.read_excel(file_pathAS, 
                          sheet_name="C1-Incomes", skiprows=3)
as_C1.columns.values[0] = 'Year'
xcols = [0] + list(range(11,20))
as_C1 = as_C1.iloc[:,xcols]
xnames = ['Year','All','Bottom 50%','Middle 40%','Top 10%','Top 5%','Top 1%','Top 0.5%','Top 0.1%','Top 0.01%']
for i,name in enumerate(xnames):
    as_C1.columns.values[i] = name    # There should be an easier way to rename columns

def isNaN(num):
    return num != num
x1 = isNaN(as_C1.loc[:,'All'])
x2 = isNaN(as_C1.loc[:,'Year'])
x3 = x1 + x2
as_C1 = as_C1.loc[~x3,:]    # Clear out rows with nan (but not the first two, which have some data)
as_C1.set_index('Year',drop=False,inplace=True)  # Do not drop, so it will be in merged df

asref = pd.read_excel(file_pathAS, sheet_name="C0-Ref Stats", skiprows=1)
asref.columns = asref.iloc[0]
asref = asref.drop(0).reset_index(drop=True).apply(pd.to_numeric, errors='coerce')
x1 = isNaN(asref.loc[:,'Year'])
asref = asref.loc[~x1,:]
x1 = isNaN(asref.iloc[0,:])
asref = asref.loc[:,~x1]
asref.set_index('Year',drop=True,inplace=True)  # Yes drop, so it does not duplicate in merge

as_merged = as_C1.merge(asref,left_index=True,right_index=True)#,suffixes=('','_btinc'))

for i,quantile in enumerate(quantiles):    # Convert incomes to per-capita, real
    as_merged.loc[:,quantile] = 1000 * as_merged.loc[:,quantile] \
        / as_merged.loc[:,'N. indivs.            (filing & non-fil.)'] \
        * as_merged.loc[:,'PCE'] 

dfdict[names[3]] = as_merged


#%% Populate final table dataframe

for i,quantile in enumerate(quantiles):
    for j,name in enumerate(names):
        x1 = dfdict[name]
        table1.loc[name,quantile] = 100*(x1.loc[years[1],quantile] - x1.loc[years[0],quantile]) / x1.loc[years[0],quantile]
  
    
#%% Old  


print(table1)

fig, ax = plt.subplots(figsize=(8, 2))  
ax.axis('tight')
ax.axis('off')

table = ax.table(cellText=table1.values, colLabels=table1.columns, rowLabels=table1.index, cellLoc='center', loc='center')

plt.show(ax)

with PdfPages('figures/table1.pdf') as pdf:
    pdf.savefig(fig)
    plt.close()
