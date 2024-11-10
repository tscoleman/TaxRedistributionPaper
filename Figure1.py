##########################################
# Script for creating Figure 1 from      #
# Tax Progressivity paper                #
# "Taxable Income as a Fraction of Pre-  #
#   Tax Hybrid Income (PSZ data)"        #
##########################################

'''
Overview
-------------
- Figure 1
- "Taxable Income as a Fraction of Pre-Tax Hybrid Income (PSZ data)"
- Data from PSZ spreadsheet
- Need to set file_path to the appropriate file path


Requirements
-------------


'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib as mpl
import seaborn as sns
import os
from cycler import cycler


sns.set(style="whitegrid")

#file_path = "C:\\Users\\decla\\Downloads\\PSZ2022AppendixTablesII(Distrib).xlsx"
file_path = "/Users/tcoleman/tom/Economics/Harris/research/IncomeInequality/AS_PSZdata/PSZ2022AppendixTablesII(Distrib).xlsx"
file_path = "PSZ2022AppendixTablesII(Distrib).xlsx"

#%% Read in data and process

# The 'categories' list must match the sheet from the PSZ workbook
# Put them in this order so that 
cat_names =['bottom 50%','Middle 40%','Top 10%'] # ['Top 10%','Middle 40%','bottom 50%']# ['bottom 50%','Middle 40%','Top 10%']
label_names = ['Bottom 50%','Middle 40%','Top 10%'] # This is really silly, but PSZ have lc 'bottom' in their spreadsheet so rename
sheet_names = ['TD7','TD8','TD9'] # ['TD9','TD8','TD7']# ['TD7','TD8','TD9'] 
sheets = []
for catname,sheetname in zip(cat_names,sheet_names):
    x1 = pd.read_excel(file_path, sheet_name=sheetname,header=7,index_col=0)
    sheets.append(x1)
#TD8 = pd.read_excel(file_path, sheet_name="TD8",header=7,index_col=0)
#TD9 = pd.read_excel(file_path, sheet_name="TD9",header=7,index_col=0)
TB3 = pd.read_excel(file_path, sheet_name="TB3",header=7,index_col=0)
TD5 = pd.read_excel(file_path, sheet_name="TD5",header=7,index_col=0)

income_df = pd.DataFrame(sheets[0].loc[:,'equal-split individuals'])
income_df.columns = [cat_names[0]]
income_df[cat_names[1]] = sheets[1].loc[:,'equal-split individuals']
income_df[cat_names[2]] = sheets[2].loc[:,'equal-split individuals']
income_df['All_FI'] = TD5.loc[:,'Individuals']
for i, catname in enumerate(cat_names):       # Fiscal income by tax units
    income_df[cat_names[i]+'_taxunits'] = sheets[i].loc[:,'Tax units']
income_df['All_taxunits'] = TD5.loc[:,'Tax units']

income_df.index.name = "Year"

income_df = income_df.merge(TB3,left_index=True,right_index=True,suffixes=('','_TB3'))

for i, catname in enumerate(cat_names):
    income_df[cat_names[i]+'_share'] = income_df[catname] / income_df[catname+'_TB3']

'''
shares_df = pd.DataFrame(TD9.loc[:,'equal-split individuals']/TB3.loc[:,'Top 10%'])
shares_df.columns = ['Top 10%']
shares_df['Middle 40%'] = TD8.loc[:,'equal-split individuals']/TB3.loc[:,'Middle 40%']
shares_df['Bottom 50%'] = TD7.loc[:,'equal-split individuals']/TB3.loc[:,'bottom 50%']
shares_df.index.name = "Year"
'''

shares_df = income_df[[x+'_share' for x in cat_names]]   # make new df with only shares
shares_df.columns = label_names

x1 = list(range(1962,2020))
shares_df = shares_df.loc[x1,:]   # df for plotting, with shares only
x1 =[1979,2014]
growth_df = income_df.copy()    # Growth for Fiscal Income by adult
growth_df = growth_df.loc[x1,['All_FI']+cat_names]    # Calculate growth for Fiscal Income
growth_df.loc['PSZ Fiscal Inc Adult'] = 100*(growth_df.loc[x1[1]]/growth_df.loc[x1[0]] - 1)
x2 = [x+'_TB3' for x in cat_names]   # Now for NI
growth_df.loc[x1] = income_df.loc[x1,['All']+x2]
growth_df.loc['PSZ Pre-Tax'] = 100*(growth_df.loc[x1[1]]/growth_df.loc[x1[0]] - 1)
x2 = [x+'_taxunits' for x in cat_names]   # Now for FI by tax units
growth_df.loc[x1] = income_df.loc[x1,['All_taxunits']+x2]
growth_df.loc['PSZ FI Tax Units'] = 100*(growth_df.loc[x1[1]]/growth_df.loc[x1[0]] - 1)
#shares_df.plot()
#plt.show()
#plt.close()
print(growth_df)


#%% 

 
#sns.lineplot(data=data_melted, x="Year", y="Percentage", hue="Type", linewidth=0.8)
plt.rcParams['font.size'] = '30'
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
# These colors are orange, green, blue (put in this order so that "bottom 50%" comes out solid blue but the legend is first)
plt.rcParams['axes.prop_cycle'] = (cycler(linestyle=['solid','dashed','dashdot']) + cycler(color=[ '#1f77b4','#ff7f0e', '#2ca02c']))
# This cycles over linestyles and colors:
# Linestyles see https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html
# The linestyles here are "solid, dotted, dashed, dashdot, long dash with offset, dashdotdotted"
# The colors here are black plus the first six from standard matplotlib color (see https://www.statology.org/matplotlib-default-colors/)
# or https://matplotlib.org/stable/users/prev_whats_new/dflt_style_changes.html#colors-in-default-property-cycle
# roughly black, blue, orange, green, red, purple
#plt.rcParams['axes.prop_cycle'] = (cycler(linestyle=["-",":","--","-.", (5, (10, 3)),(0, (3, 5, 1, 5, 1, 5))]) 
#                                   + cycler(color=[ '#000000','#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']))
#plt.rcParams['lines.linestyle'] = 'dashed'
plt.grid(axis='x',alpha=.0)
plt.grid(axis='y',alpha=.25)

#plt.figure(figsize=(10, 6),frameon=False,clear=True)

plt.plot(shares_df)
plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{x:.0%}'))
#plt.locator_params(axis='y', nbins=8)

plt.title("Figure 1: Fiscal Income as a Fraction of Pre-Tax Hybrid Income\nPSZ data, 1960-2019")
plt.ylabel("Share (%)")
#plt.xlabel("Years")
#plt.legend(shares_df.columns.to_list(),frameon=False)#, loc='lower center')#,ncol=3)
plt.legend(shares_df.columns.to_list(),loc='upper center', bbox_to_anchor=(0.5, -0.1),
          fancybox=True, shadow=True, ncol=3,fontsize=11)

plt.tight_layout()

plt.savefig('figures/figure1_output.pdf')
plt.show()
plt.close()

#print(os.getcwd())

## %%

#shares_df.plot()


# %%
