##############################################
#Reads AS,  -- Produces Figure 6 & Figure 7 #
##############################################
'''
Overview
-------------
- Figure 6
- "Growth in real before- and after-tax-and-transfer income"
- Data from Auten & Splinter spreadsheet 'Output2'
- Consistent rankings
- Need to set file_path to the appropriate file path

- Figure 7
- "Growth in real before and after-tax and transfer income (PSZ)"
- Data from Piketty & Saez spreadsheet
- Need to set file_path to the appropriate file path
- Non-Consistent rankings
Requirements

- AS real is indexed to 2019, PSZ real is 2018. But the base year for
  deflation does not matter, since we are measuring relative growth from 1966

-------------


'''

#%% Imports
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from cycler import cycler

#%% Formatting for graphs
plt.rcParams['font.size'] = '15'
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
# These colors are blue,orange (put in this order so that "Before Tax" comes out solid blue)
plt.rcParams['axes.prop_cycle'] = (cycler(linestyle=['solid','dashed']) + cycler(color=[  '#1f77b4','#ff7f0e']))
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

#%% Various utility functions
# Need this to test for NaN (numpy or math will not work because includes strings)
def isNaN(num):
    return num != num


def plot_AScombined_panels(file_path, sheet_name, ref_sheet, indexyr):
    # Set up the plot
    fig, axs = plt.subplots(2, 2, figsize=(14, 11))
     
    # Load the data
    # It would be better if python had a read_xls function like R, where one could specify rows to read
    data_output2 = pd.read_excel(file_path, sheet_name=sheet_name)
    xdata = pd.read_excel(file_path, sheet_name=ref_sheet, header=None)

    data_pretax = data_output2.iloc[3:64,2:]   # Read just the rows we want (rows 5:65, with 5 being headers)
                                               # But remember python indexes from zero, so it is python rows 4:64. So why 3??
    data_pretax = data_pretax.dropna()
    data_pretax.columns = data_pretax.iloc[0]    # Sets columns from headings in Excel sheet
    data_pretax = data_pretax.drop(index=data_pretax.iloc[0].name)  # This will drop the 0th row, which were put into column names
    data_pretax.set_index('year',drop=False,inplace=True)  # use year as index
    
# Need this to test for NaN (numpy or math will not work because includes strings)
    def isNaN(num):
        return num != num
    x1 = isNaN(xdata.iloc[2,:])
    xdata2 = xdata.loc[:,~x1]
    xdata2.columns = xdata2.iloc[2]
    data_ref = xdata2.dropna()
    data_ref=data_ref.rename(columns = {'Year':'year'})
    data_ref.set_index('year',drop=False,inplace=True)  # use year as index
    
    data_comb = pd.concat([data_pretax, data_ref], axis=1, join="inner") # This is one dataframe with all data
    # Growth, indexed to index year, for before tax income
    pctl_graph = ['bottomQ','middleQ','topQ','top1%']
    pctl_graph_name = ['Bottom Quintile','Middle Quintile','Top Quintile','Top 1%']
    beftax_pctl = ['q1noneg','q3','q5','i5'] # NB A&S use 'noneg' for bottom quintile, in their sheet C1a-Quin and C7a-Redis
    # Loop over the desired quintiles to calculate growth, indexed to 1.0 in 'indexyr'
    for graph_name, pctl in zip(pctl_graph,beftax_pctl):
        data_comb[graph_name+'_b'] = data_comb.loc[:,pctl] *data_comb.loc[:,'PCE'] / data_comb.loc[:,'N. indivs.            (filing & non-fil.)']
        data_comb[graph_name+'_b'] = data_comb[graph_name+'_b'] / data_comb.loc[indexyr,graph_name+'_b']

    # Now need to do after-tax income, which means combining various columns
    # Make list of names for calculating AS 'Redistribution Rate'
    #   RedRate (our 'Implied Tax Rate') = sum of
    #      f (Col CD ...) 'Federal income tax (less ref. credits)'
    #      st (col CL ...) 'State income tax'
    #      x (col CT ...) 'Corp tax'
    #      p (col DB ...) 'Property taxes'
    #      o (col DR ...) 'Other taxes'  
    #      wt (col DJ ...) 'Payroll taxes'
    #      es (col EH ...) 'Estate taxes' 
    #    less
    #      s (col BN ...) 'SS+UI benefits'
    #      mc (col EX ...) 'Medicare benefits'
    #      ca (col FF ...) 'Cash transfers'
    #      nc (col FN ...) 'Non-cash transfers'
    #  Divided by Pre-tax Income 
    #      i 'Income by Percentiles'
    #      q 'Income by Quintiles'
    # 
    # This definition is taken from AS's sheet 'C7a-Redis' which does it for quintiles, 
    # and then the definition is extended to the percentiles
    # (But in that sheet overall income comes from sheet 'C1-Incomes' for Percentiles, from 'C1a-Quin' for Quintiles))
    
    # This is all done by pre-tax income groups, which is the first block (rows 5:65) in 'Output2'
    xafttaxadd = ['s','mc','ca','nc']
    xafttaxsub = ['f','st','x','p','o','wt','es']
    # Checking the numbers in sheets 'C1-Incomes' versus 'Output2'
    # Compare the total for 1962 in 'C1-Incomes' versus the sume of 'Bottom 50%'+'50% to 90%'+'Top 10%' in 'Output2'
    # Everything matches except 'Sales and other taxes' vs Col 'o'
    # To go from 'Pre-Tax Income' to 'Pre-Tax Plus Transfer' in C1-Incomes, Add:
    #   'Social Security benefits (321)' + 'UI benefits (322)' = Col 's' in 'Output2' (15,158.00)
    #   'Cash welfare and tax credits (323)' = Col 'ca' (7,835)
    #   'Medicare (324)' = Col 'mc' (0 for 1962, 686 for 1966)
    #   'Other transfers (325)' = col 'nc' (1,435)
    # To go from 'Pre-Tax Plus Transfer' to 'After-tax (before Gov't Cons)' in C1-Incomes, Subtract:
    #   'Fed Income and Estate Taxes (401)' = Col 'f' + 'es' (44,111.42)
    #   'State/Local Income Taxes (402)' = Col 'st'  (2,536.3)
    #   'Corporate Income Taxes (403)' = Col 'x' (20,988.00)
    #   'Property Taxes (404)' = Col 'p' (16,238.00)
    #   'Payroll Taxes(405)' = Col 'wt' (16,444.00)
    #   'Sales and other taxes (406)' = Col 'o' (21,902 in C1-Incomes, 28,905 in Output2)

    # Need to have this stupid two lists because A&S don't have quite consistent naming convention
    #   Starting income labeled i1, i2 for percentiles and q1, q2 for quintiles
    #   while income subcategories are labeled f1, f2, ... and fq1, fq2, ... for quintiles
    afttax_pctl = ['q1','q3','q5','5']
#    xquintilesa = ['q1','q2','q3','q4','q5','5']
#    xquintilesb = ['q1','q2','q3','q4','q5','i5']  
    
# Loop over the desired quintiles, and for each quintile sum up the adds and subs for
# different incomes to go from before-tax to after-transfer&tax
    for graph_name, pctlb, pctla in zip(pctl_graph,beftax_pctl,afttax_pctl):
        xlista = [namea+pctla+'_Sum' for namea in xafttaxadd]  # list comprehension to build list of adding incomes
        xlists = [names+pctla+'_Sum' for names in xafttaxsub]  # list comprehension to build list of adding incomes
        data_comb[graph_name+'_a'] = data_comb[pctlb] + (data_comb[xlista].sum(axis=1) - data_comb[xlists].sum(axis=1))/1000000
    # Now calculate growth, indexed to 1.00 in 'indexyr'
        data_comb[graph_name+'_a'] = data_comb[graph_name+'_a'] *data_comb.loc[:,'PCE'] / data_comb.loc[:,'N. indivs.            (filing & non-fil.)']
        data_comb[graph_name+'_a'] = data_comb[graph_name+'_a'] / data_comb.loc[indexyr,graph_name+'_a']    

#    pctl_graph_name = ['Bottom Quintile','Middle Quintile','Top Quintile','Top 1%']
#    pctl_graph = ['bottomQ','middleQ','topQ','top1%']
    xrow = [0,0,1,1] # Stupid way to keep track of indexes into the graph 'axs'
    xcol = [0,1,0,1]

# Bottom Quintile (Top-left)
    for rowi,coli,pctlid,pctlname in zip(xrow,xcol,pctl_graph,pctl_graph_name):
#        axs[rowi,coli].plot(data_comb['year'], data_comb[pctlid+'_b'], label='Before Tax')
#        axs[rowi,coli].plot(data_comb['year'], data_comb[pctlid+'_a'], label='After Tax')
        axs[rowi,coli].plot(data_comb[['year',pctlid+'_b',pctlid+'_a']])#,label=['Before Tax','After Tax'])
        axs[rowi,coli].set_title(pctlname)
        axs[rowi,coli].set_xlabel(' ')
        axs[rowi,coli].set_ylim(0.5,3)
        axs[rowi,coli].grid(axis='y',alpha=0.25)  # Only horizontal gridlines
        
#    axs[0,0].legend(['Before Tax','After Tax'],frameon=False)                   # Legend in the upper left
    fig.legend(['Before Tax','After Tax'],loc='upper center', bbox_to_anchor=(0.5, 0.02),
          fancybox=True, shadow=True, ncol=4)#,fontsize=11)
    axs[0,1].axes.yaxis.set_ticklabels([])           # Turn off left axis for the right-hand graphs
    axs[0,1].spines[['left']].set_visible(False)
    axs[1,1].axes.yaxis.set_ticklabels([])
    axs[1,1].spines[['left']].set_visible(False)
    axs[0,0].set_ylabel('Growth (indexed to 1 in 1966)')
    axs[1,0].set_ylabel('Growth (indexed to 1 in 1966)')



    fig.suptitle('Figure 6: Growth in real (2018) before- and after-tax-and-transfer income',fontsize=20)
    plt.tight_layout()
#    plt.show()  This command must come after 'plt.savefit()'



def avgquantile_psz(xpsz_pctl, xprobs):
    """
    Calculates average income for desired quantiles from PSZ data.

    Args:
        xpsz_pctl: DataFrame containing PSZ data (from TB4 or TC4).
        xprobs: List of desired quantiles (e.g., [0.5, 0.9, 1.0]).

    Returns:
        DataFrame containing average income for each quantile.
    """

# Need this to test for NaN (numpy or math will not work because includes strings)
    def isNaN(num):
        return num != num
    x1 = isNaN(xpsz_pctl.iloc[2,:])
    xpsz_pctl = xpsz_pctl.loc[:,~x1]
    xpsz_pctl.columns = xpsz_pctl.iloc[0]
    xpsz_pctl = xpsz_pctl.dropna()
    xyear = xpsz_pctl.columns[1:]
    # Drop last (deflator) rows
    #xpsz_pctl = xpsz_pctl.iloc[:-1]

    xpsz_pctl = xpsz_pctl.rename(columns={xpsz_pctl.columns[0]: 'percentile'})  # Rename first column
    xpsz_pctl = xpsz_pctl[xpsz_pctl['percentile'] != 'Deflator']  # Remove last row
    xpsz_pctl['percentile'] = pd.to_numeric(xpsz_pctl['percentile']) / 100  # Convert to numeric percentiles
    xpsz_pctl['probability'] = xpsz_pctl['percentile']



    # Calculate probability mass for each percentile entry
    xpsz_pctl['probability'].iloc[:-1] = xpsz_pctl['percentile'].iloc[1:].values - xpsz_pctl['percentile'].iloc[:-1].values
    xpsz_pctl['probability'].iloc[-1] = 1 - xpsz_pctl['percentile'].iloc[-1]

    # Select only income columns - this is done before
    x1 = xpsz_pctl.drop(columns=['probability', 'percentile'])
    # Multiply by probability
    xavg_prob = x1.values * xpsz_pctl['probability'].values[:, None]

    # Cumulative sum for each column
    xcumavg = xavg_prob.cumsum(axis=0)
    # Cumulate probabilities
    xcumprob = xpsz_pctl['probability'].cumsum()

    # Find rows matching desired quantiles
    x3 = xprobs == np.round(xcumprob.values[:, None],12)
    # Sum across columns to identify matching rows
    x5 = x3.sum(axis=1)
    x1 = np.arange(0,len(x5))
    x2 = x1[x5 == 1].tolist()  # Get row indices
    # Extract desired cumulative weighted average income
    x3 = xcumavg[x2, :]
    # Calculate differences for quantiles
    x4 = np.diff(x3,prepend=0,axis=0)
    # Differences for probabilities
    x7 = pd.Series(xprobs).diff().fillna(pd.Series(xprobs).iloc[0]).to_numpy()
    # Calculate average within each quantile
    xavg = x4 / x7[:,None]

    # Transpose and format output
    xavg = xavg.T
    xavg = pd.DataFrame(xavg)
    xavg.columns = 100 * pd.Series(xprobs)
    xavg['year'] = xyear
    xavg.set_index('year',inplace=True)

    return xavg



def plot_PSZcombined_panels(file_path, sheet_name, indexyr,all4=False):
    # Set up the plot
    if all4:
        fig, axs = plt.subplots(2, 2, figsize=(14, 11))
    else:
        fig, axs = plt.subplots(1, 2, figsize=(14, 5.5))


    # Define quantiles and column names
    xprobs = [0.2, 0.4, 0.6, 0.8, 1.0]
    
    # Read pre-tax income data
    psz_pctl_beftax = pd.read_excel(file_path, sheet_name=sheet_name, skiprows=6)  # Adjust skiprows if needed
    # Calculate average by selected quantiles (assuming you have the avgquantile_psz function defined) 
    # Converted to real inside the 'avgquantile_psz' function
    psz_avgquantile_beftax = avgquantile_psz(psz_pctl_beftax, xprobs)
    # Calculate top 1% separately
    x1 = avgquantile_psz(psz_pctl_beftax, [0.5, 0.99, 1])
    psz_avgquantile_beftax['top1%'] = x1[100]
    psz_avgquantile_beftax.columns = ["q1_bef", "q2_bef", "q3_bef", "q4_bef", "q5_bef", "t1_bef"]
    
    # Read post-tax income data
    psz_pctl_afttax = pd.read_excel(file_path, sheet_name="TC4", skiprows=6)  # Adjust skiprows if needed
    # Calculate average by selected quantiles
    # Converted to real inside the 'avgquantile_psz' function
    psz_avgquantile_afttax = avgquantile_psz(psz_pctl_afttax, xprobs)
    # Calculate top 1% separately
    x1 = avgquantile_psz(psz_pctl_afttax, [0.5, 0.99, 1])
    psz_avgquantile_afttax['top1%'] = x1[100]
    psz_avgquantile_afttax.columns = ["q1_aft", "q2_aft", "q3_aft", "q4_aft", "q5_aft", "t1_aft"]


    
    data_comb = pd.concat([psz_avgquantile_beftax,psz_avgquantile_afttax], axis=1, join="inner") # This is one dataframe with all data
    data_comb['year'] = data_comb.index
    # Growth, indexed to index year, for before tax income
    if all4:
        pctl_graph = ['q1','q3','q5','t1']
        pctl_graph_name = ['Bottom Quintile','Middle Quintile','Top Quintile','Top 1%']
    else:
        pctl_graph = ['q1','q3']
        pctl_graph_name = ['Bottom Quintile','Middle Quintile']
    # Loop over the desired quintiles to calculate growth, indexed to 1.00 in 'indexyr'
    for pctl in pctl_graph:
        data_comb[pctl+'_bef'] = data_comb[pctl+'_bef'] / data_comb.loc[indexyr,pctl+'_bef']
        data_comb[pctl+'_aft'] = data_comb[pctl+'_aft'] / data_comb.loc[indexyr,pctl+'_aft']

    if all4:
        xrow = [0,0,1,1] # Stupid way to keep track of indexes into the graph 'axs'
        xcol = [0,1,0,1]
    
    # Bottom Quintile (Top-left)
        for rowi,coli,pctlid,pctlname in zip(xrow,xcol,pctl_graph,pctl_graph_name):
    #        axs[rowi,coli].plot(data_comb['year'], data_comb[pctlid+'_b'], label='Before Tax')
    #        axs[rowi,coli].plot(data_comb['year'], data_comb[pctlid+'_a'], label='After Tax')
            axs[rowi,coli].plot(data_comb[['year',pctlid+'_aft',pctlid+'_bef']])#,label=['Before Tax','After Tax'])
            axs[rowi,coli].set_title(pctlname)
            axs[rowi,coli].set_xlabel(' ')
            axs[rowi,coli].set_ylim(0.5,3)
            axs[rowi,coli].grid(axis='y',alpha=0.25)  # Only horizontal gridlines
            
        fig.legend(['Before Tax','After Tax'],loc='upper center', bbox_to_anchor=(0.5, 0.02),
          fancybox=True, shadow=True, ncol=4)#,fontsize=11)        axs[0,1].axes.yaxis.set_ticklabels([])           # Turn off left axis for the right-hand graphs
        axs[0,1].spines[['left']].set_visible(False)
        axs[1,1].axes.yaxis.set_ticklabels([])
        axs[1,1].spines[['left']].set_visible(False)
        axs[0,0].set_ylabel('Growth (indexed to 1 in 1966)')
        axs[1,0].set_ylabel('Growth (indexed to 1 in 1966)')

    else:
# Bottom Quintile (Top-left)
        for i,pctlid,pctlname in zip(range(len(pctl_graph)),pctl_graph,pctl_graph_name):
            axs[i].plot(data_comb[['year',pctlid+'_aft',pctlid+'_bef']])#,label=['Before Tax','After Tax'])
            axs[i].set_title(pctlname)
            axs[i].set_xlabel(' ')
            axs[i].set_ylim(0.5,3)
            axs[i].grid(axis='y',alpha=0.25)  # Only horizontal gridlines
            
        fig.legend(['Before Tax','After Tax'],loc='upper center', bbox_to_anchor=(0.5, 0.02),
          fancybox=True, shadow=True, ncol=4)#,fontsize=11)        axs[1].axes.yaxis.set_ticklabels([])           # Turn off left axis for the right-hand graphs
        axs[1].spines[['left']].set_visible(False)
        axs[0].set_ylabel('Growth (indexed to 1 in 1966)')



    if sheet_name == 'TB4':
        fig.suptitle('Figure 7: Growth in real before and after-tax and transfer income (PSZ)',fontsize=20)
    elif sheet_name == 'TA4':
        fig.suptitle('Figure 7b: Growth in real factor vs after-tax and transfer income (PSZ)',fontsize=20)
    else:
        fig.suptitle('Figure 7c: Unknown (PSZ)',fontsize=20)
    plt.tight_layout()
#    plt.show()  This command must come after 'plt.savefit()'


#%% Run plots


file_path = "C:\\Users\\decla\\Downloads\\"
file_path = '/Users/tcoleman/tom/Economics/Harris/research/IncomeInequality/AS_PSZdata/'
file_path = ''
file_name = 'AutenSplinter-IncomeIneq_2024.xlsx'
sheet_name = 'Output2'  
sheet_name_output = 'Output'
ref_sheet = 'C0-Ref Stats'
PCE_col = 23  # Column index for PCE values
pop_col = 16  # Column index for population values
base_row_PCE = 1  # Base row for PCE values

plot_AScombined_panels(file_path+file_name, sheet_name, ref_sheet, 1966)
plt.savefig('figures/figure6_output.pdf',bbox_inches='tight')
plt.show()    # Must be after 'plt.savefig()'
plt.close()


file_name = 'PSZ2022AppendixTablesII(Distrib).xlsx'
plot_PSZcombined_panels(file_path+file_name, 'TB4', 1966)
plt.savefig('figures/figure7_output.pdf',bbox_inches='tight')
plt.show()    # Must be after 'plt.savefig()'
plt.close()
plot_PSZcombined_panels(file_path+file_name, 'TB4', 1966,all4=True)
plt.savefig('figures/figure7all4_output.pdf',bbox_inches='tight')
plt.show()    # Must be after 'plt.savefig()'
plt.close()
plot_PSZcombined_panels(file_path+file_name, 'TA4', 1966)
plt.savefig('figures/figure7b_output.pdf',bbox_inches='tight')
plt.show()    # Must be after 'plt.savefig()'
plt.close()
plot_PSZcombined_panels(file_path+file_name, 'TA4', 1966,all4=True)
plt.savefig('figures/figure7ball4_output.pdf',bbox_inches='tight')
plt.show()    # Must be after 'plt.savefig()'
plt.close()



import os
print(os.getcwd())
