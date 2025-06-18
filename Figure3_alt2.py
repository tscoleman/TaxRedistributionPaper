##########################################
# This reads data from Auten & Splinter  #
# Piketty, Saez, Zuchman. Versus         #
# Figure23.py this compares AS vs PSZ for#
# not-consistent rankings (and including #
# gov't consumption)                     #
##########################################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler


# This should run under the directory with both code and data (.xlsx files)
file_path = ''
cbofile_path = ''

# Cycler and spines to get formatting for graphs consistent
plt.rcParams['font.size'] = '12'
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
# These colors are orange, green, blue (put in this order so that "bottom 50%" comes out solid blue)
#plt.rcParams['axes.prop_cycle'] = (cycler(linestyle=['dashed','dashdot','solid']) + cycler(color=[ '#ff7f0e', '#2ca02c','#1f77b4']))
# This cycles over linestyles and colors:
# Linestyles see https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html
# The linestyles here are "solid, dotted, dashed, dashdot, long dash with offset, dashdotdotted"
# The colors here are black plus the first six from standard matplotlib color (see https://www.statology.org/matplotlib-default-colors/)
# or https://matplotlib.org/stable/users/prev_whats_new/dflt_style_changes.html#colors-in-default-property-cycle
# roughly black, blue, orange, green, red, purple
plt.rcParams['axes.prop_cycle'] = (cycler(linestyle=["-",":","--","-.", (5, (10, 3)),(0, (3, 5, 1, 5, 1, 5))]) 
                                   + cycler(color=[ '#000000','#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']))
plt.grid(axis='x',alpha=.0)
plt.grid(axis='y',alpha=.25)


#%% Read and process Auten & Splinter data for first graph (compare vs PSZ)
# -----------------------------------------
# Load and process Auten & Splinter data
# -----------------------------------------


rows_pretax = range(4, 65)
as_C1 = pd.read_excel(file_path + "AutenSplinter-IncomeIneq_2024.xlsx", 
                          sheet_name="C1-Incomes", skiprows=3)#, nrows=len(rows_pretax))
# Drop the trailing columns and some leading columns
as_C1.drop([63,64,65,66],inplace=True)
as_C1.drop([0,1,2],inplace=True)
as_C1.columns.values[0] = 'year'

as_merged = as_C1[['year']].copy()
aspercnames = ['Bottom 50%', 'Middle 40%', 'Top 10%', 'Top 1%']

colsbt = [12,13,14,15]
colsat = [32,33,34,35]

for colbt,colat,name in zip(colsbt,colsat,aspercnames):
    as_merged[name] = 100*(as_C1.iloc[:,colbt] - as_C1.iloc[:,colat]) / as_C1.iloc[:,colbt]


# Define ymin and ymax for AS data
ymin, ymax = -80, 40

#%% Load PSZ data
# -----------------------------------------
# Load and process Piketty, Saez, Zucman (PSZ) data
# -----------------------------------------


psz_sheetnos = ['7','8','9','10']  # The sheets for bottom 50%, middle 405, top 10%, top 1%
pszpercnames = ['Bottom 50%','Middle 40%','Top 10%','Top 1%']
# Loop through sheets
psz_sheets_factor = []   # empty list to hold sheets
psz_sheets_bt = []   # empty list to hold sheets
psz_sheets_at = []   # empty list to hold sheets
for sheet in psz_sheetnos:
    xfactor = pd.read_excel(file_path + "PSZ2022AppendixTablesII(Distrib).xlsx", sheet_name='TA'+sheet,skiprows=7)
    xfactor.columns.values[0] = 'year'
    psz_sheets_factor.append(xfactor)
    xat = pd.read_excel(file_path + "PSZ2022AppendixTablesII(Distrib).xlsx", sheet_name='TC'+sheet,skiprows=7)
    xat.columns.values[0] = 'year'
    psz_sheets_at.append(xat)
    xbt = pd.read_excel(file_path + "PSZ2022AppendixTablesII(Distrib).xlsx", sheet_name='TB'+sheet,skiprows=7)
    xbt.columns.values[0] = 'year'
    psz_sheets_bt.append(xbt)

psz_merged_factor = xfactor[['year']].copy()
psz_merged_bt = xfactor[['year']].copy()

for i,name in enumerate(pszpercnames):
    psz_merged_factor[name] = 100 * (psz_sheets_factor[i]['equal-split individuals'] 
                              - psz_sheets_at[i]['equal-split individuals']) / psz_sheets_factor[i]['equal-split individuals']
    psz_merged_bt[name] = 100 * (psz_sheets_bt[i]['equal-split individuals'] 
                              - psz_sheets_at[i]['equal-split individuals']) / psz_sheets_bt[i]['equal-split individuals']
    


# Define ymin and ymax for PSZ data
ymin_psz, ymax_psz = -55, 55


#%% Plot first figure (A&S vs PSZ factor income)

# First Figure: AS data and PSZ data (with AS income groups)
fig1, axs1 = plt.subplots(1, 2, figsize=(12, 6))
fig1.suptitle('Figure A2: Before less After-Tax Income, Not Consistent Rankings\nPSZ (Factor Income, 1962-2019) v. AS (1960-2019)')
# AS data (left subplot)
for percname in aspercnames:
    axs1[0].plot(as_merged['year'], as_merged[percname], label=percname)

axs1[0].set_ylabel('%')
axs1[0].set_title('Auten & Splinter')
# Place legend in _figure_ which puts it below both subplots
# Put it here (after the first subplot) so it uses only the labels from first subplot
# See https://stackoverflow.com/questions/4700614/how-to-put-the-legend-outside-the-plot
fig1.legend(loc='upper center', bbox_to_anchor=(0.5, 0.02),
          fancybox=True, shadow=True, ncol=4,fontsize=11)

axs1[0].set_ylim(ymin, ymax)
axs1[0].set_xlim(1960, 2020)
axs1[0].grid(axis='y', alpha=0.25)
axs1[0].grid(axis='x', alpha=0)


# PSZ data (right subplot) with same income groups as AS
for percname in pszpercnames:
    if percname in psz_merged_factor.columns:
        axs1[1].plot(psz_merged_factor['year'], psz_merged_factor[percname], label=percname)
'''
if 'Bottom50taxtr' in psz_transfers.columns:
    axs1[1].plot(psz_transfers['year'], 100 * psz_transfers['Bottom50taxtr'], label='Bottom 50%', color='blue')
if 'Middle40taxtr' in psz_transfers.columns:
    axs1[1].plot(psz_transfers['year'], 100 * psz_transfers['Middle40taxtr'], label='Middle 40%', color='red')
if 'Top10taxtr' in psz_transfers.columns:
    axs1[1].plot(psz_transfers['year'], 100 * psz_transfers['Top10taxtr'], label='Top 10%', color='black')
if 'Top1taxtr' in psz_transfers.columns:
    axs1[1].plot(psz_transfers['year'], 100 * psz_transfers['Top1taxtr'], label='Top 1%', color='green')
'''
axs1[1].set_ylabel('')
axs1[1].set_title('Piketty, Saez, Zucman')
axs1[1].set_ylim(ymin,ymax)
axs1[1].set_xlim(1960, 2020)
axs1[1].grid(axis='y', alpha=0.25)
axs1[1].grid(axis='x', alpha=0)
axs1[1].axes.yaxis.set_ticklabels([])
axs1[1].spines[['left']].set_visible(False)



# Adjust layout for the first figure
plt.tight_layout()
# totally silly, but need 'bbox_inches='tight'' to force legend to be put into figure
# See https://stackoverflow.com/questions/4700614/how-to-put-the-legend-outside-the-plot
plt.savefig('figures/figureA2_output.pdf',bbox_inches="tight") 
plt.show()
plt.close()


#%% Plot second figure (A&S vs PSZ before-tax income)

# First Figure: AS data and PSZ data (with AS income groups)
fig2, axs2 = plt.subplots(1, 2, figsize=(12, 6))
fig2.suptitle('Figure A1: Before less After-Tax Income, Not Consistent Rankings\nPSZ (Before Tax Hybrid Income, 1962-2019) v. AS (1960-2019)')
# AS data (left subplot)
for percname in aspercnames:
    axs2[0].plot(as_merged['year'], as_merged[percname], label=percname)

axs2[0].set_ylabel('%')
axs2[0].set_title('Auten & Splinter')
# Place legend in _figure_ which puts it below both subplots
# Put it here (after the first subplot) so it uses only the labels from first subplot
# See https://stackoverflow.com/questions/4700614/how-to-put-the-legend-outside-the-plot
fig2.legend(loc='upper center', bbox_to_anchor=(0.5, 0.02),
          fancybox=True, shadow=True, ncol=4,fontsize=11)

axs2[0].set_ylim(ymin, ymax)
axs2[0].set_xlim(1960, 2020)
axs2[0].grid(axis='y', alpha=0.25)
axs2[0].grid(axis='x', alpha=0)


# PSZ data (right subplot) with same income groups as AS
for percname in pszpercnames:
    if percname in psz_merged_bt.columns:
        axs2[1].plot(psz_merged_bt['year'], psz_merged_bt[percname], label=percname)

axs2[1].set_ylabel('')
axs2[1].set_title('Piketty, Saez, Zucman')
axs2[1].set_ylim(ymin,ymax)
axs2[1].set_xlim(1960, 2020)
axs2[1].grid(axis='y', alpha=0.25)
axs2[1].grid(axis='x', alpha=0)
axs2[1].axes.yaxis.set_ticklabels([])
axs2[1].spines[['left']].set_visible(False)



# Adjust layout for the first figure
plt.tight_layout()
# totally silly, but need 'bbox_inches='tight'' to force legend to be put into figure
# See https://stackoverflow.com/questions/4700614/how-to-put-the-legend-outside-the-plot
plt.savefig('figures/figureA1_output.pdf',bbox_inches="tight") 
plt.show()
plt.close()


