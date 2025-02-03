########################################################
# This reads data from Auten & Splinter, PSZ, and CBO  #
# produces Figure 5 "Auten & Splinter and CBO Reynolds−Smolensky Index" #
# Uses some unique local filepaths, e.g. CBOData.xlsx  #   
########################################################



import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler



#sns.lineplot(data=data_melted, x="Year", y="Percentage", hue="Type", linewidth=0.8)
# To get these to work, may need to restart kernel
plt.rcParams['font.size'] = '12'
#plt.rcParams.update({'font.size': 15})
#plt.rcParams['font.size'] = 15  # Note that none of these work to change fontsize, contrary to what Gemini and StackOverflow recommend
# Changing the figsize seems to be the best way to change fonts, etc
plt.rcParams['axes.spines.right'] = False
plt.rcParams['axes.spines.top'] = False
# These colors are blue, green, orange 
plt.rcParams['axes.prop_cycle'] = (cycler(linestyle=['solid','dashdot','dashed']) + cycler(color=[ '#1f77b4', '#2ca02c','#ff7f0e']))
# This cycles over linestyles and colors:
# Linestyles see https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html
# The linestyles here are "solid, dotted, dashed, dashdot, long dash with offset, dashdotdotted"
# The colors here are black plus the first six from standard matplotlib color (see https://www.statology.org/matplotlib-default-colors/)
# or https://matplotlib.org/stable/users/prev_whats_new/dflt_style_changes.html#colors-in-default-property-cycle
# roughly black, blue, orange, green, red, purple
#plt.rcParams['axes.prop_cycle'] = (cycler(linestyle=["-",":","--","-.", (5, (10, 3)),(0, (3, 5, 1, 5, 1, 5))]) 
#                                   + cycler(color=[ '#000000','#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']))
#plt.rcParams['lines.linestyle'] = 'dashed'
# These colors are orange, green, blue (put in this order so that "bottom 50%" comes out solid blue but the legend is first)
plt.rcParams['axes.prop_cycle'] = (cycler(linestyle=['solid','dashed','dashdot']) + cycler(color=[ '#1f77b4','#ff7f0e', '#2ca02c']))
plt.rcParams['axes.prop_cycle'] = (cycler(linestyle=["-",":","--","-.", (5, (10, 3)),(0, (3, 5, 1, 5, 1, 5))]) 
                                   + cycler(color=[ '#000000','#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']))

plt.grid(axis='x',alpha=.0)
plt.grid(axis='y',alpha=.25)


#%%m Gini Utility Functions

# --------------------------
# Section 0: Gini Utility Functions
# --------------------------

# Function to calculate Gini coefficient from density
def gini_tsc(ydensity, xpctl):
    ydensity_cum = np.cumsum(ydensity, axis=1)
    
    # Trim ydensity_cum to match ydensity dimensions
    if ydensity_cum.shape[1] != ydensity.shape[1]:
        ydensity_cum = ydensity_cum[:, :-1]
    
    x1 = ydensity.shape
    ydensity_cum = np.zeros(x1)     # Make an array of zeros of the correct size
    x3 = np.cumsum(ydensity, axis=1)  # Cumulative sum, but we want to 'offset' and make the left-most column as zeros
    ydensity_cum[:,1:x1[1]] = x3[:,0:x1[1]-1]  # This puts the left-most as zero and drops the right-most

    z1 = np.multiply(xpctl, ydensity_cum + 0.5 * ydensity)
    z2 = np.sum(z1, axis=1)
# Definition of Gini is A/A+B where 
#   A+B = area below 45deg = 1/2
#   A = area between 45 & actual distribution
#   B = area below actual distribution
# The z2 I calculated is B, so Gini is (1/2 - z2) / (1/2)
    return 2 * (0.5 - z2)

# Function to calculate Gini coefficient from PSZ data
def gini_psz(yavginc_matrix, xpercentile):
  # This assume data from sheets TB3 and TC3, which are the average income by percentile 
  # But we have to take the average income and convert to the income for that percentile, and then
  # divide by the total to get the income density
  # yavginc_matrix is the average income by percentile, with years along columns (and perecntiles rows)
  # xpercentile is the cumulative percentile (in sheet TB4 as percent but already converted to decimal)
    y1 = np.diff(np.append(xpercentile, 1))
    y2 = yavginc_matrix * y1[:, np.newaxis]
    total_income = np.sum(y2, axis=0)
    income_density = y2 / total_income
    return gini_tsc(income_density.T, y1)



#%%mPSZ Data Processing

# --------------------------
# Section 1: PSZ Data Processing
# --------------------------


# Function to load PSZ data and calculate RS index
def load_psz_data_and_calculate(psz_filename,sheet_name):
    psz_beftax = pd.read_excel(psz_filename, sheet_name = sheet_name, header=None, skiprows=7).dropna(how='all', axis=1)
    psz_afttax = pd.read_excel(psz_filename, sheet_name = 'TC4', header=None, skiprows=7).dropna(how='all', axis=1)

# Need this to test for NaN (numpy or math will not work because includes strings)
    def isNaN(num):
        return num != num
    # Clean up by removing end columns (with na) and bottom row (which is deflator)
    x1 = isNaN(psz_beftax.iloc[1,:])
    psz_beftax = psz_beftax.loc[:,~x1]
    psz_beftax.columns = psz_beftax.iloc[0]
    psz_beftax.dropna(inplace=True)
    psz_beftax = psz_beftax.iloc[0:-1,:]
    # Thie first column is the percentile. Convert this to the mass and put in a new column
    psz_beftax.columns.values[0] = 'percentile'
    x1 = isNaN(psz_afttax.iloc[1,:])
    psz_afttax = psz_afttax.loc[:,~x1]
    psz_afttax.columns = psz_afttax.iloc[0]
    psz_afttax.dropna(inplace=True)
    psz_afttax = psz_afttax.iloc[0:-1,:]
    psz_afttax.columns.values[0] = 'percentile'

    psz_percentile = np.array(psz_beftax.loc[:,'percentile']) / 100.
    psz_beftax_np = np.array(psz_beftax.iloc[:,1:])
    # Replace negative with zero
    psz_beftax_np[psz_beftax_np < 0] = 0
    psz_beftax_gini = gini_psz(psz_beftax_np,psz_percentile)
    psz_afttax_np = np.array(psz_afttax.iloc[:,1:])
    # Replace negative with zero
    psz_afttax_np[psz_afttax_np < 0] = 0
    psz_afttax_gini = gini_psz(psz_afttax_np,psz_percentile)

#xxx
    # Make a dummy np array to hold year, before-tax, and after-tax gini
    psz_gini = np.array(psz_beftax.iloc[0:4,1:]).T
    psz_gini[:,1] = psz_beftax_gini
    psz_gini[:,2] = psz_afttax_gini
    psz_gini[:,3] = psz_beftax_gini - psz_afttax_gini
    psz_gini[:,0] = psz_beftax.columns[1:].astype(int)
    
    # Convert to a dataframe, and name columns and create index
    psz_gini = pd.DataFrame(psz_gini)
    psz_gini.columns = ['year','psz_gini_beftax','psz_gini_afttax','psz_gini_diff']
    psz_gini.set_index('year',drop=False,inplace=True)  # use year as index


    return psz_gini

#%% CBO Data Processing

# --------------------------
# Section 2: CBOData Processing
# --------------------------

# Function to calculate Gini coefficient
def gini_coefficient(data):
    sorted_data = np.sort(data)
    n = len(sorted_data)
    index = np.arange(1, n + 1)
    gini = (np.sum((2 * index - n - 1) * sorted_data)) / (n * np.sum(sorted_data))
    return gini

# Function to load CBOData and calculate RS index
def load_cbo_data_and_calculate(cbo_filename):
    
# Use the workbook 58353-supplemental-data.xlsx because the share data are sorted in a way that is easy to read
# Note that for this workbook data are all sorted and ranked by before-tax income (for all income concepts)
# From the documentation to this workbook:
#    "Income groups are created by ranking households by income before transfers and taxes, adjusted for household size. A household consists of people sharing a housing unit, regardless of their relationships. Each income quintile (fifth) contains approximately equal numbers of people. If a household has negative income (that is, if its business or investment losses are larger than its other income), it is excluded from the lowest income group but included in the totals."

# Read in ranked by pre-tax income

#cbo_share_mktinc <- read.xlsx(xlsxFile="/Users/tcoleman/tom/Economics/Harris/research/IncomeInequality/AS_PSZdata/CBO2019-additional-data-for-researchers/58353-supplemental-data.xlsx",sheet="10. Household Income Shares",rows=rows_mktinc)


    xdata = pd.read_excel(cbo_filename, sheet_name = '10. Household Income Shares')
    cbo_names = ['mkt','beftax','afttax']
    cbo_rows = [list(range(11,52)),list(range(54,95)),list(range(97,138))]
# We need rows 11, and:
    # Market income: 13:53, which means 11:52 (because of python's stupidity of indexing from zero, and range not going over the ragne but one shorter)
    # Before-tax: 56:96, which means 54:95
    # Aftet-tax: 99:139, which means 97:138
    cbo_df = list()
    for row in cbo_rows:
        df = xdata.iloc[[9]+row,:]
        df = df.dropna(axis=1)
        df.columns = df.iloc[0]  # This sets column names to the headers
        df = df.iloc[1:,:]   # Drop the first row (which are now column names)
        df.rename(columns={'Year':'year'},inplace=True)   # Rename column to lower-case 'year' to match with other dataframes
        # An alternative (using location rather than name):
        # df.columns.values[0] = ['year']
        df.set_index('year',drop=False,inplace=True)  # use year as index
        df.iloc[:,1:] = df.iloc[:,1:] / 100       # convert from percentage to decimal
    # Clean income_group names
        df.rename(columns={
            'Lowest Quintile':'Bot Quin',
            'Second Quintile\t':'2nd Quin',
            'Middle Quintile\t':'3rd Quin',
            'Fourth Quintile\t': '4th Quin', 
            'Highest Quintile':'Top Quin',
            '81st to 90th Percentiles':'81-90 Pctl', 
            '91st to 95th Percentiles':'91-95 Pctl',
            '96th to 99th Percentiles':'96-99 Pctl',
            'Top 1 Percent':'Top 1%'
            },inplace=True)           
        cbo_df.append(df)

    cbo_mkt = cbo_df[0]
    cbo_beftax = cbo_df[1]
    cbo_afttax = cbo_df[2]
        
    cbo_percentile = pd.Series(np.array([0,1,.2,.2,.2,.2,.2,.1,.05,.04,.01]))
    cbo_percentile.index = cbo_mkt.columns
    cbo_shares_used = ['Bot Quin', '2nd Quin','3rd Quin', '4th Quin', 
           '81-90 Pctl', '91-95 Pctl','96-99 Pctl', 'Top 1%']
    
    cbo_gini = cbo_mkt[['year','All Quintiles']]   # Make just a dummy dataframe (with the right index)
    y7 = gini_tsc(np.array(cbo_mkt[cbo_shares_used]),np.array(cbo_percentile[cbo_shares_used]))
    cbo_gini['gini_mkt'] = y7
    y7 = gini_tsc(np.array(cbo_beftax[cbo_shares_used]),np.array(cbo_percentile[cbo_shares_used]))
    cbo_gini['gini_beftax'] = y7
    y7 = gini_tsc(np.array(cbo_afttax[cbo_shares_used]),np.array(cbo_percentile[cbo_shares_used]))
    cbo_gini['gini_afttax'] = y7
    cbo_gini['RSIndex_cbo_mkt'] = cbo_gini['gini_mkt'] - cbo_gini['gini_afttax']
    cbo_gini['RSIndex_cbo_bef'] = cbo_gini['gini_beftax'] - cbo_gini['gini_afttax']
        
    return cbo_gini

#%% AS Data Processing

# --------------------------
# Section 3: Auten & Splinter (AS) Data Processing
# --------------------------

# Function to load Auten & Splinter data and calculate RS index
def load_auten_splinter_data_and_calculate(as_filename):
    df = pd.read_excel(as_filename, sheet_name = 'Output')
    # Rows in spreadsheet:
        #                                       Excel    Python rows 
        # PS income replication:                7-66      python: 5-65
        # Pre-tax income:                       71-130    python: 69:129
        # After-transfer, before tax:           135-194   python: 133:193
        # After-tax-transfer (incl gov't cons)  199-258   python: 197:257 (note there is an extra row for 2019)
    
    data_beftax = df.iloc[69:129,2:]   # Read just the rows we want (rows 71:130, with 2 being headers)
                                               # But remember python indexes from zero, so it is python rows 69:129. So why 3??
    data_beftax = data_beftax.dropna()
    data_beftax.columns = df.iloc[2][2:]  # This sets column names to the headers
    #   But Auten & Splinter do not put into the headers the names for the addtional Gini columns that appear for pre-tax 
    #   income, and only put those names into row 70 (69) of their spreadsheet. Annoying and we have to do this work-around
    data_beftax.columns.values[31:35] = ['After-tax income', 'After-tax income before deficits/govt consumption (Reynolds-Smolensky index)','RS transfers only','Gini not sz adj']
    # Calculate Reynolds-Smolensky index as Auten & Splinter do in sheet F-B19 and their Figure B19. 
    # Here we are comparing Before-Tax vs After-Tax-Transfer but before Government Consumption
    data_beftax.set_index('year',drop=False,inplace=True)  # use year as index
    data_beftax['RSIndex_AS'] = data_beftax['Gini not sz adj'] - data_beftax['After-tax income before deficits/govt consumption (Reynolds-Smolensky index)']

    data_afttax = df.iloc[197:257,2:]   # Read just the rows we want (rows 135:194, with 5 being headers)
                                               # But remember python indexes from zero, so it is python rows 4:64. So why 3??
    data_afttax.columns = df.iloc[2][2:]  # This sets column names to the headers
# Need this to test for NaN (numpy or math will not work because includes strings)
    def isNaN(num):
        return num != num
    # Clean up by removing end columns (with na) and bottom row (which is deflator)
    x1 = isNaN(data_afttax.iloc[0,:])
    data_afttax = data_afttax.loc[:,~x1]
    data_afttax = data_afttax.dropna()
    data_afttax.set_index('year',drop=False,inplace=True)  # use year as index

    data_beftax['as_gini_diff'] = data_beftax['gini'] - data_afttax['gini']
    
    return data_beftax



#%% Main

# --------------------------
# Section 6: Main Execution
# --------------------------

#def main():
    # File paths
#    psz_file_path = "C:\\Users\\decla\\Downloads\\PSZ2022AppendixTablesII(Distrib).xlsx"
#    cbo_file_path = "C:\\Users\\decla\\Downloads\\TSC_Additions_LawPaper.xlsx"
#    as_file_path = "C:\\Users\\decla\\Downloads\\AutenSplinter-Calculations67a.xlsx"

file_path = "C:\\Users\\decla\\Downloads\\"
file_path = '/Users/tcoleman/tom/Economics/Harris/research/IncomeInequality/AS_PSZdata/'
#file_path = ''
pszname = "PSZ2022AppendixTablesII(Distrib).xlsx"
cboname = "CBO2019-additional-data-for-researchers/58353-supplemental-data.xlsx"
#cboname = "58353-supplemental-data.xlsx"
asname = "AutenSplinter-IncomeIneq_2024.xlsx"
psz_filename = file_path+pszname
cbo_filename = file_path+cboname
as_filename = file_path+asname


# Process PSZ data
ginis_psz = load_psz_data_and_calculate(psz_filename,sheet_name='TB4')
print("PSZ Data Processed:")
print(ginis_psz.head())

# Process CBOData
rs_cbo = load_cbo_data_and_calculate(cbo_filename)
print("CBO Data Processed:")
print(rs_cbo.head())

# Process Auten & Splinter Data
rs_as = load_auten_splinter_data_and_calculate(as_filename)
print("Auten & Splinter Data Processed:")
print(rs_as.head())

rs_df = pd.concat([rs_as, ginis_psz, rs_cbo], axis=1, join="outer") # This is one dataframe with all data
rs_df = rs_df.sort_index()

# Use this to scale the figures, which then scales all the fonts, etc
figscale = .9
plt.figure(figsize=(figscale*10,figscale*6))  # Changing the figsize seems to be the best way to change fonts, etc
plt.plot(rs_df[['RSIndex_AS','RSIndex_cbo_mkt','psz_gini_diff']])
plt.title('Figure 5: Auten & Splinter and CBO Reynolds−Smolensky Index\nAS 1960-2019, CBO 1979-2019, PSZ 1962-2019',fontsize=15)
#plt.title('Auten & Splinter and CBO Reynolds−Smolensky Index')

plt.legend(['Auten&Splinter','CBO','PSZ (Gini diff)'],loc='upper center', bbox_to_anchor=(0.5, -.1),
          fancybox=False, shadow=False, ncol=3)#,fontsize=11)
plt.grid(axis='x',alpha=.0)
plt.grid(axis='y',alpha=.25)
#plt.savefig('figures/figure5_output.pdf',bbox_inches='tight')  # The 'bbbox_inches='tight'' makes sure the legend is withing the .pdf
plt.show()

plt.figure(figsize=(figscale*10,figscale*6))
plt.plot(rs_df[['RSIndex_AS','as_gini_diff','psz_gini_diff']])
plt.title('Comparison of A&S and PSZ for Gini Differences',fontsize=15)
plt.legend(['A&S Reynolds-Smolensky','A&S (Gini diff)','PSZ (Gini diff)'],loc='upper center', bbox_to_anchor=(0.5, -0.1),
          fancybox=False, shadow=False, ncol=3)#,fontsize=11)
plt.grid(axis='x',alpha=.0)
plt.grid(axis='y',alpha=.25)
#plt.savefig('figures/figure5b_output.pdf',bbox_inches='tight')
plt.show()


#%% Run for 'alt' versions that use PSZ Factor income rather than pre-tax hybrid income (matching NI)

# The 'alt' versions use PSZ Factor income from sheet TA4. Just comment out the 'TB4' version
# And also the legends below
ginis_psz = load_psz_data_and_calculate(psz_filename,sheet_name='TA4')

rs_df = pd.concat([rs_as, ginis_psz, rs_cbo], axis=1, join="outer") # This is one dataframe with all data
rs_df = rs_df.sort_index()

# Use this to scale the figures, which then scales all the fonts, etc
figscale = 0.7
plt.figure(figsize=(figscale*10,figscale*6))  # Changing the figsize seems to be the best way to change fonts, etc
plt.plot(rs_df[['RSIndex_AS','RSIndex_cbo_mkt','psz_gini_diff']])
plt.title('Figure A3: Auten & Splinter and CBO Reynolds−Smolensky Index\nAS 1960-2019, CBO 1979-2019, PSZ 1962-2019',fontsize=15)
#plt.title('Auten & Splinter and CBO Reynolds−Smolensky Index')

plt.legend(['Auten&Splinter','CBO','PSZ (Gini diff, factor income)'],loc='upper center', bbox_to_anchor=(0.5, -.1),
          fancybox=False, shadow=False, ncol=3)#,fontsize=11)
plt.grid(axis='x',alpha=.0)
plt.grid(axis='y',alpha=.25)
#plt.savefig('figures/figureA3_output.pdf',bbox_inches='tight')  # The 'bbbox_inches='tight'' makes sure the legend is withing the .pdf
plt.show()

plt.figure(figsize=(figscale*10,figscale*6))
plt.plot(rs_df[['RSIndex_AS','as_gini_diff','psz_gini_diff']])
plt.title('Figure A4:Alternate Comparison of A&S and PSZ for Gini Differences\nAS 1960-2019, PSZ 1962-2019')
plt.legend(['A&S Reynolds-Smolensky','A&S (Gini diff)','PSZ (Gini diff, factor income)'],loc='upper center', bbox_to_anchor=(0.5, -0.1),
          fancybox=False, shadow=False, ncol=3)#,fontsize=11)
plt.grid(axis='x',alpha=.0)
plt.grid(axis='y',alpha=.25)
#plt.savefig('figures/figureA4_output.pdf',bbox_inches='tight')
plt.show()



