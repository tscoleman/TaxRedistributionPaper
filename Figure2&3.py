##########################################
# This reads data from Auten & Splinter  #
# Piketty, Saez, Zuchman, and CBO and    #
# produces Figures 3 and 4               #
##########################################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler


# Change the following file_paths by commenting out the ones that are not required
# but please leave them in so they don't need to be re-entered
file_path = "C:\\Users\\decla\\Downloads\\"
cbofile_path = "C:\\Users\\decla\\Downloads\\"
file_path = '/Users/tcoleman/tom/Economics/Harris/research/IncomeInequality/AS_PSZdata/'
cbofile_path = '/Users/tcoleman/tom/Economics/Harris/research/IncomeInequality/AS_PSZdata/CBO2019-additional-data-for-researchers/CBO_distribution_household_income_2019_data/'
#file_path = ''
#cbofile_path = ''

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
#plt.rcParams['lines.linestyle'] = 'dashed'
plt.grid(axis='x',alpha=.0)
plt.grid(axis='y',alpha=.25)


#%% Read and process Auten & Splinter data for first graph (compare vs PSZ)
# -----------------------------------------
# Load and process Auten & Splinter data
# -----------------------------------------


rows_pretax = range(4, 65)
as_beftax = pd.read_excel(file_path + "AutenSplinter-IncomeIneq_2024.xlsx", 
                          sheet_name="Output2", skiprows=rows_pretax[0], nrows=len(rows_pretax))


'''
 Read in Data from Auten & Splinter Quintile and other percentiles. Read in from sheet "Output2" which has ranked by 
 pre-tax, pre-tax / after-transfer, after-tax / after-transfer
 Key to variable names:
  Percentiles 
    1 = P0-50
    2 = P50-90
    3 = top 10%
    4 = top 5%
    5 = top 1%
    6 = top 0.5%
    7 = top 0.1%
    8 = top 0.01%
  Quintiles:
    1, 2, 3, 4, 5 = 1st, ... 20% (quintile)
  Income definitions / type
    itot & i1-8 = pre-tax national income by percentile
    q1-q5 = pre-tax national income by quintiles
  For the following, replace '#' with 1, 2, 3, ... for percentiles, and q1, q2, ... for quintiles
    ac# & aqc# = minimum income thresholds (percentile & quintile)
    w#_Sum & wq#_Sum = taxable wages
    i#_Sum & iq#_Sum = interest + non-taxable interest
    d#_Sum & dq#_Sum = taxable dividends
    e#_Sum & eq#_Sum = passthrough
    s#_Sum & sq#_Sum = SS+UI benefits 
             Equals "Social Security benefits (321)" plus "UI benefits (322)" in sheet C1-Incomes
    c#_Sum & cq#_Sum = Corp. retained earnings
    f#_Sum & fq#_Sum = Federal income tax (less refundable credits)
    st#_Sum & stq#_Sum = State income tax
    x#_Sum & xq#_Sum = Corporate tax
    p#_Sum & pq#_Sum = Property taxes
    wt#_Sum & wtq#_Sum = Payroll taxes
    o#_Sum & oq#_Sum = Other taxes
    r#_Sum & rq#_Sum = Retirement
    es#_Sum & esq#_Sum = Estate taxes
    wi#_Sum & wiq#_Sum = ESI and Payroll taxes (employer and employee portions)
    mc#_Sum & mcq#_Sum = Medicare benefits
    ca#_Sum & caq#_Sum = Cash transfers
    nc#_Sum & ncq#_Sum = Non-cash transfers



 Data in sheet "Output2" are organized into three blocks (with each block skipping years 1961, 1963, 1965)
  Rows 6-65: Ranked by pre-tax income (matches National Income)
  Rows 74-133: Ranked by pre-tax / after-transfer income
  Rows 139-198: Ranked by after-tax / after-transfer income (matches National Income)

 The columns in the sheet "output2" are messy and confusing. The following 4 lines are the column headings in a .csv format:
  Row 1: Excel column 
  Row 2: Income category headings
  Row 3: Precentile / quintile headings
  Row 4: specific variable names
 These can be copied to a text editor (and the initial '#' comment character stripped off) then saved as a .csv and read in to Excel to help read the column headings
A,B,C,D,E,F,G,H,I,J,K,L,M,N,O,P,Q,R,S,T,U,V,W,X,Y,Z,AA,AB,AC,AD,AE,AF,AG,AH,AI,AJ,AK,AL,AM,AN,AO,AP,AQ,AR,AS,AT,AU,AV,AW,AX,AY,AZ,BA,BB,BC,BD,BE,BF,BG,BH,BI,BJ,BK,BL,BM,BN,BO,BP,BQ,BR,BS,BT,BU,BV,BW,BX,BY,BZ,CA,CB,CC,CD,CE,CF,CG,CH,CI,CJ,CK,CL,CM,CN,CO,CP,CQ,CR,CS,CT,CU,CV,CW,CX,CY,CZ,DA,DB,DC,DD,DE,DF,DG,DH,DI,DJ,DK,DL,DM,DN,DO,DP,DQ,DR,DS,DT,DU,DV,DW,DX,DY,DZ,EA,EB,EC,ED,EE,EF,EG,EH,EI,EJ,EK,EL,EM,EN,EO,EP,EQ,ER,ES,ET,EU,EV,EW,EX,EY,EZ,FA,FB,FC,FD,FE,FF,FG,FH,FI,FJ,FK,FL,FM,FN,FO,FP,FQ,FR,FS,FT,FU,FV,FW,FX,FY,FZ,GA,GB,GC,GD,GE,GF,GG,GH,GI,GJ,GK,GL,GM,GN,GO,GP,GQ,GR,GS,GT,GU,GV,GW,GX,GY,GZ,HA,HB,HC,HD,HE,HF,HG,HH,HI,HJ,HK,HL,HM,HN,HO,HP,HQ,HR,HS,HT,HU,HV,HW,HX,HY,HZ,IA,IB,IC,ID,IE,IF,IG,IH,II,IJ,IK,IL,IM,IN,IO,IP,IQ,IR,IS,IT,IU,IV,IW,IX,IY,IZ,JA,JB,JC,JD,JE,JF,JG
,,,,,,Total,1=P0-50,2=P50-90,3=top 10%,4=Top 5%,5=top 1%,6=top 0.5%,7=top 0.1%,8=Top 0.01%,Quintiles,,,,,,Minimum Income Thresholds,,,,,,,Quintile Thresholds,,,,Gini,taxable wages,,,,,,,,interest + non-taxable interest,,,,,,,,taxable dividends,,,,,,,,passthrough ,,,,,,,,SS+UI benefits,,,,,,,,Corp. retained earnings,,,,,,,,Federal income tax (less ref. credits),,,,,,,,State income tax,,,,,,,,Corp tax,,,,,,,,Property taxes,,,,,,,,Payroll taxes,,,,,,,,Other taxes,,,,,,,,Retirement ,,,,,,,,estate taxes,,,,,,,,ESI and Payroll taxes (employer and employee portions),,,,,,,,Medicare benefits,,,,,,,,Cash transfers ,,,,,,,,Non-cash transfers ,,,,,,,,taxable wages,,,,,interest + non-taxable interest,,,,,taxable dividends,,,,,passthrough ,,,,,SS+UI benefits,,,,,Corp. retained earnings,,,,,"Federal income tax (less ref. credits, that is including ref credits)",,,,,State income tax,,,,,Corp tax,,,,,Property taxes,,,,,Payroll taxes,,,,,Other taxes,,,,,Retirement ,,,,,estate taxes,,,,,ESI and Payroll taxes (employer and employee portions),,,,,Medicare benefits,,,,,Cash transfers ,,,,,Non-cash transfers ,,,,
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,Bottom 50%,50% to 90%,Top 10%,Top 5%,Top 1%,Top 0.5%,Top 0.1%,Top 0.01%,Bottom 50%,50% to 90%,Top 10%,Top 5%,Top 1%,Top 0.5%,Top 0.1%,Top 0.01%,Bottom 50%,50% to 90%,Top 10%,Top 5%,Top 1%,Top 0.5%,Top 0.1%,Top 0.01%,Bottom 50%,50% to 90%,Top 10%,Top 5%,Top 1%,Top 0.5%,Top 0.1%,Top 0.01%,Bottom 50%,50% to 90%,Top 10%,Top 5%,Top 1%,Top 0.5%,Top 0.1%,Top 0.01%,Bottom 50%,50% to 90%,Top 10%,Top 5%,Top 1%,Top 0.5%,Top 0.1%,Top 0.01%,Bottom 50%,50% to 90%,Top 10%,Top 5%,Top 1%,Top 0.5%,Top 0.1%,Top 0.01%,Bottom 50%,50% to 90%,Top 10%,Top 5%,Top 1%,Top 0.5%,Top 0.1%,Top 0.01%,Bottom 50%,50% to 90%,Top 10%,Top 5%,Top 1%,Top 0.5%,Top 0.1%,Top 0.01%,Bottom 50%,50% to 90%,Top 10%,Top 5%,Top 1%,Top 0.5%,Top 0.1%,Top 0.01%,Bottom 50%,50% to 90%,Top 10%,Top 5%,Top 1%,Top 0.5%,Top 0.1%,Top 0.01%,Bottom 50%,50% to 90%,Top 10%,Top 5%,Top 1%,Top 0.5%,Top 0.1%,Top 0.01%,Bottom 50%,50% to 90%,Top 10%,Top 5%,Top 1%,Top 0.5%,Top 0.1%,Top 0.01%,Bottom 50%,50% to 90%,Top 10%,Top 5%,Top 1%,Top 0.5%,Top 0.1%,Top 0.01%,Bottom 50%,50% to 90%,Top 10%,Top 5%,Top 1%,Top 0.5%,Top 0.1%,Top 0.01%,Bottom 50%,50% to 90%,Top 10%,Top 5%,Top 1%,Top 0.5%,Top 0.1%,Top 0.01%,Bottom 50%,50% to 90%,Top 10%,Top 5%,Top 1%,Top 0.5%,Top 0.1%,Top 0.01%,Bottom 50%,50% to 90%,Top 10%,Top 5%,Top 1%,Top 0.5%,Top 0.1%,Top 0.01%,Bot quintile,2nd quintile,3rd quintile,4th quintile,Top quintile,Bot quintile,2nd quintile,3rd quintile,4th quintile,Top quintile,Bot quintile,2nd quintile,3rd quintile,4th quintile,Top quintile,Bot quintile,2nd quintile,3rd quintile,4th quintile,Top quintile,Bot quintile,2nd quintile,3rd quintile,4th quintile,Top quintile,Bot quintile,2nd quintile,3rd quintile,4th quintile,Top quintile,Bot quintile,2nd quintile,3rd quintile,4th quintile,Top quintile,Bot quintile,2nd quintile,3rd quintile,4th quintile,Top quintile,Bot quintile,2nd quintile,3rd quintile,4th quintile,Top quintile,Bot quintile,2nd quintile,3rd quintile,4th quintile,Top quintile,Bot quintile,2nd quintile,3rd quintile,4th quintile,Top quintile,Bot quintile,2nd quintile,3rd quintile,4th quintile,Top quintile,Bot quintile,2nd quintile,3rd quintile,4th quintile,Top quintile,Bot quintile,2nd quintile,3rd quintile,4th quintile,Top quintile,Bot quintile,2nd quintile,3rd quintile,4th quintile,Top quintile,Bot quintile,2nd quintile,3rd quintile,4th quintile,Top quintile,Bot quintile,2nd quintile,3rd quintile,4th quintile,Top quintile,Bot quintile,2nd quintile,3rd quintile,4th quintile,Top quintile
_TYPE_,_FREQ_,year,filingtype,incometype,ranktype,itot,i1,i2,i3,i4,i5,i6,i7,i8,q1noneg,q2,q3,q4,q5,q1wneg,ac2,ac3,ac4,ac5,ac6,ac7,ac8,aqc2,aqc3,aqc4,aqc5,gini,w1_Sum,w2_Sum,w3_Sum,w4_Sum,w5_Sum,w6_Sum,w7_Sum,w8_Sum,i1_Sum,i2_Sum,i3_Sum,i4_Sum,i5_Sum,i6_Sum,i7_Sum,i8_Sum,d1_Sum,d2_Sum,d3_Sum,d4_Sum,d5_Sum,d6_Sum,d7_Sum,d8_Sum,e1_Sum,e2_Sum,e3_Sum,e4_Sum,e5_Sum,e6_Sum,e7_Sum,e8_Sum,s1_Sum,s2_Sum,s3_Sum,s4_Sum,s5_Sum,s6_Sum,s7_Sum,s8_Sum,c1_Sum,c2_Sum,c3_Sum,c4_Sum,c5_Sum,c6_Sum,c7_Sum,c8_Sum,f1_Sum,f2_Sum,f3_Sum,f4_Sum,f5_Sum,f6_Sum,f7_Sum,f8_Sum,st1_Sum,st2_Sum,st3_Sum,st4_Sum,st5_Sum,st6_Sum,st7_Sum,st8_Sum,x1_Sum,x2_Sum,x3_Sum,x4_Sum,x5_Sum,x6_Sum,x7_Sum,x8_Sum,p1_Sum,p2_Sum,p3_Sum,p4_Sum,p5_Sum,p6_Sum,p7_Sum,p8_Sum,wt1_Sum,wt2_Sum,wt3_Sum,wt4_Sum,wt5_Sum,wt6_Sum,wt7_Sum,wt8_Sum,o1_Sum,o2_Sum,o3_Sum,o4_Sum,o5_Sum,o6_Sum,o7_Sum,o8_Sum,r1_Sum,r2_Sum,r3_Sum,r4_Sum,r5_Sum,r6_Sum,r7_Sum,r8_Sum,es1_Sum,es2_Sum,es3_Sum,es4_Sum,es5_Sum,es6_Sum,es7_Sum,es8_Sum,wi1_Sum,wi2_Sum,wi3_Sum,wi4_Sum,wi5_Sum,wi6_Sum,wi7_Sum,wi8_Sum,mc1_Sum,mc2_Sum,mc3_Sum,mc4_Sum,mc5_Sum,mc6_Sum,mc7_Sum,mc8_Sum,ca1_Sum,ca2_Sum,ca3_Sum,ca4_Sum,ca5_Sum,ca6_Sum,ca7_Sum,ca8_Sum,nc1_Sum,nc2_Sum,nc3_Sum,nc4_Sum,nc5_Sum,nc6_Sum,nc7_Sum,nc8_Sum,wq1_Sum,wq2_Sum,wq3_Sum,wq4_Sum,wq5_Sum,iq1_Sum,iq2_Sum,iq3_Sum,iq4_Sum,iq5_Sum,dq1_Sum,dq2_Sum,dq3_Sum,dq4_Sum,dq5_Sum,eq1_Sum,eq2_Sum,eq3_Sum,eq4_Sum,eq5_Sum,sq1_Sum,sq2_Sum,sq3_Sum,sq4_Sum,sq5_Sum,cq1_Sum,cq2_Sum,cq3_Sum,cq4_Sum,cq5_Sum,fq1_Sum,fq2_Sum,fq3_Sum,fq4_Sum,fq5_Sum,stq1_Sum,stq2_Sum,stq3_Sum,stq4_Sum,stq5_Sum,xq1_Sum,xq2_Sum,xq3_Sum,xq4_Sum,xq5_Sum,pq1_Sum,pq2_Sum,pq3_Sum,pq4_Sum,pq5_Sum,wtq1_Sum,wtq2_Sum,wtq3_Sum,wtq4_Sum,wtq5_Sum,oq1_Sum,oq2_Sum,oq3_Sum,oq4_Sum,oq5_Sum,rq1_Sum,rq2_Sum,rq3_Sum,rq4_Sum,rq5_Sum,esq1_Sum,esq2_Sum,esq3_Sum,esq4_Sum,esq5_Sum,wiq1_Sum,wiq2_Sum,wiq3_Sum,wiq4_Sum,wiq5_Sum,mcq1_Sum,mcq2_Sum,mcq3_Sum,mcq4_Sum,mcq5_Sum,caq1_Sum,caq2_Sum,caq3_Sum,caq4_Sum,caq5_Sum,ncq1_Sum,ncq2_Sum,ncq3_Sum,ncq4_Sum,ncq5_Sum
'''


print("Columns in as_beftax:", as_beftax.columns)

if 'Year' in as_beftax.columns:
    as_beftax.rename(columns={'Year': 'year'}, inplace=True)

xredisadd = ['f', 'st', 'x', 'p', 'o', 'wt', 'es']
xredissub = ['s', 'mc', 'ca', 'nc']
xpercentiles = ['1', '2', '3', '5']   # This specifies which percentiles to calculate
aspercnames = ['Bottom 50%', 'Middle 40%', 'Top 10%', 'Top 1%']


as_redis = as_beftax[['year']]
as_redis = pd.concat([as_redis, as_beftax[['i' + x for x in xpercentiles]]], axis=1)

for i in range(len(xpercentiles)):
    add_cols = [col + xpercentiles[i] + '_Sum' for col in xredisadd if col + xpercentiles[i] + '_Sum' in as_beftax.columns]
    sub_cols = [col + xpercentiles[i] + '_Sum' for col in xredissub if col + xpercentiles[i] + '_Sum' in as_beftax.columns]
    print(f"Adding columns for {xpercentiles[i]}: {add_cols}")
    print(f"Subtracting columns for {xpercentiles[i]}: {sub_cols}")
    
    if add_cols and sub_cols:
        x1 = as_beftax[add_cols].sum(axis=1)
        x2 = as_beftax[sub_cols].sum(axis=1)
        as_redis['redisamt' + aspercnames[i]] = (x1 - x2) / 1000000
        as_redis['redisrate' + aspercnames[i]] = 100 * (x1 - x2) / 1000000 / as_redis['i' + xpercentiles[i]]

# Define ymin and ymax for AS data
if all(col in as_redis.columns for col in ['redisrateMiddle40', 'redisrateBot50', 'redisrateTop10', 'redisrateTop1']):
    ymin = min(as_redis[['redisrateMiddle40', 'redisrateBot50', 'redisrateTop10', 'redisrateTop1']].min())
    ymax = max(as_redis[['redisrateMiddle40', 'redisrateBot50', 'redisrateTop10', 'redisrateTop1']].max())
else:
    ymin, ymax = -55, 55

#%% Load PSZ data
# -----------------------------------------
# Load and process Piketty, Saez, Zucman (PSZ) data
# -----------------------------------------

psz_avgpeinc = pd.read_excel(file_path + "PSZ2022AppendixTablesII(Distrib).xlsx", sheet_name="avgpeinc")  # This gets it from the back sheet but column labels not as good
psz_avgpeinc = pd.read_excel(file_path + "PSZ2022AppendixTablesII(Distrib).xlsx", sheet_name="TB3", skiprows=7)
psz_transfers = pd.read_excel(file_path + "PSZ2022AppendixTablesII(Distrib).xlsx", sheet_name="TG4d", skiprows=8)
psz_taxrates = pd.read_excel(file_path + "PSZ2022AppendixTablesII(Distrib).xlsx", sheet_name="taxrates")   # This gets it from the back sheet but column labels not as good
psz_taxrates = pd.read_excel(file_path + "PSZ2022AppendixTablesII(Distrib).xlsx", sheet_name="TG1",skiprows=8)

#psz_transfers.columns = psz_transfers.columns.str.strip().str.replace(' ', '').str.replace('.', '', regex=False)
#psz_avgpeinc.columns = psz_avgpeinc.columns.str.strip().str.replace(' ', '').str.replace('.', '', regex=False)
#psz_taxrates.columns = psz_taxrates.columns.str.strip().str.replace(' ', '').str.replace('.', '', regex=False)

# Need this to test for NaN (numpy or math will not work because includes strings)
def isNaN(num):
    return num != num
x1 = isNaN(psz_transfers.iloc[2,:])
psz_transfers = psz_transfers.loc[:,~x1]    # Clear out columns with nan
x1 = isNaN(psz_transfers.loc[:,'adult pop'])
psz_transfers = psz_transfers.loc[~x1,:]    # Clear out rows with nan (but not the first two, which have some data)
psz_transfers = psz_transfers.iloc[:,0:-1]  # clear out last column
psz_transfers.rename(columns={ psz_transfers.columns[0]: 'year' },inplace=True)
psz_transfers.set_index('year',drop=False,inplace=True)  # use year as index

x1 = isNaN(psz_avgpeinc.iloc[-2,:])
psz_avgpeinc = psz_avgpeinc.loc[:,~x1]    # Clear out columns with nan
psz_avgpeinc = psz_avgpeinc.dropna()      # Clear out rows with nan
psz_avgpeinc = psz_avgpeinc.iloc[:,0:-1]  # clear out last column
psz_avgpeinc.rename(columns={ psz_avgpeinc.columns[0]: 'year' },inplace=True)
if 'bottom 50%' in psz_avgpeinc.columns:    # Typo in label for PSZ sheet TB3
    psz_avgpeinc.rename(columns={'bottom 50%':'Bottom 50%'},inplace=True)
psz_avgpeinc.set_index('year',drop=False,inplace=True)  # use year as index

# =============================================================================
'''
psz_avgpeinc = psz_avgpeinc.dropna()
psz_avgpeinc.set_index('year',drop=False,inplace=True)  # use year as index
'''
# =============================================================================

psz_taxrates = psz_taxrates.dropna()
psz_taxrates.rename(columns={ psz_taxrates.columns[0]: 'year' },inplace=True)
psz_taxrates.set_index('year',drop=False,inplace=True)  # use year as index


print("Columns in psz_avgpeinc:", psz_avgpeinc.columns)
print("Columns in psz_transfers:", psz_transfers.columns)

# There is a bug in the PSZ sheet for the 'Middle40%' so we re-calculate
if 'Bottom90%' in psz_transfers.columns and 'Bottom50%' in psz_transfers.columns:
    psz_transfers['Middle40%'] = (0.9 * psz_transfers['Bottom90%'] - 0.5 * psz_transfers['Bottom50%']) / 0.4
else:
    print("Columns for Bottom90% or Bottom50% not found in psz_transfers. Check the data file.")

psz_merged = psz_taxrates.merge(psz_transfers,left_index=True,right_index=True,suffixes=('_taxrate','_transf'))
psz_merged = psz_merged.merge(psz_avgpeinc,left_index=True,right_index=True,suffixes=('','_btinc'))

pszpercnames = ['Bottom 50%', 'Middle 40%', 'Top 10%', 'Top 1%']

for percname in pszpercnames:  
    # calculate tax & transfer rate as taxrate (originally from TG1, df psz_taxrates) less
    #   $ transfers (originally from TG4d, df psz_transfers) divided by $ income (originally from TB3, df pszavgpeinc)
    #   Put it back into psz_merged, overwriting the pszavginc
    psz_merged[percname] = 100*(psz_merged[percname+'_taxrate'] - psz_merged[percname+'_transf'] / psz_merged[percname])


'''
columns_to_merge = ['year', 'avgpeinc2equal', 'avgpeinc3equal', 'avgpeinc4equal', 'avgpeinc8equal', 'avgpeinc9equal', 'avgpeinc10equal']
try:
    psz_transfers = psz_transfers.merge(psz_avgpeinc[columns_to_merge], on='year', how='left')
except KeyError as e:
    print(f"KeyError during merge: {e}. Ensure 'year' column exists in both DataFrames and check other column names.")

try:
    psz_transfers['Middle40trperc'] = psz_transfers['Middle40'] / psz_transfers['avgpeinc10equal']
    psz_transfers['Bottom90trperc'] = psz_transfers['Bottom90%'] / psz_transfers['avgpeinc9equal']
    psz_transfers['Bottom50trperc'] = psz_transfers['Bottom50%'] / psz_transfers['avgpeinc8equal']
    psz_transfers['Top10trperc'] = psz_transfers['Top10%'] / psz_transfers['avgpeinc2equal']
    psz_transfers['Top5trperc'] = psz_transfers['Top5%'] / psz_transfers['avgpeinc3equal']
    psz_transfers['Top1trperc'] = psz_transfers['Top1%'] / psz_transfers['avgpeinc4equal']
except KeyError as e:
    print(f"KeyError during calculation: {e}. Check the column names and data.")

columns_to_merge_tax = ['year', 'taxbot90', 'taxbot50', 'taxmiddle40', 'taxtop10', 'taxtop1']
try:
    psz_transfers = psz_transfers.merge(psz_taxrates[columns_to_merge_tax], on='year', how='left')
except KeyError as e:
    print(f"KeyError during merge: {e}. Ensure 'year' column exists in both DataFrames and check other column names.")

try:
    psz_transfers['Bottom90taxtr'] = psz_transfers['taxbot90'] - psz_transfers['Bottom90trperc']
    psz_transfers['Bottom50taxtr'] = psz_transfers['taxbot50'] - psz_transfers['Bottom50trperc']
    psz_transfers['Middle40taxtr'] = psz_transfers['taxmiddle40'] - psz_transfers['Middle40trperc']
    psz_transfers['Top10taxtr'] = psz_transfers['taxtop10'] - psz_transfers['Top10trperc']
    psz_transfers['Top1taxtr'] = psz_transfers['taxtop1'] - psz_transfers['Top1trperc']
except KeyError as e:
    print(f"KeyError during calculation: {e}. Check the column names and data.")
'''

# Define ymin and ymax for PSZ data
try:
    ymin_psz = psz_transfers[['Bottom90taxtr', 'Bottom50taxtr', 'Middle40taxtr', 'Top10taxtr', 'Top1taxtr']].min().min()
    ymax_psz = psz_transfers[['Bottom90taxtr', 'Bottom50taxtr', 'Middle40taxtr', 'Top10taxtr', 'Top1taxtr']].max().max()
except KeyError as e:
    print(f"KeyError when defining ymin_psz and ymax_psz: {e}.")
    ymin_psz, ymax_psz = -55, 55


#%% Process Auten & Splinter data
#------------------------------------
# -----------------------------------------
# Process AS data to compute quintile redistribution rates
# -----------------------------------------

# Define quintile identifiers and names
xquintiles = ['4', '5', '6', '7', '8']  # Adjust these identifiers based on your data
xquintile_names = ['Quintile1', 'Quintile2', 'Quintile3', 'Quintile4', 'Quintile5']

# Initialize DataFrame to store the results
as_quintiles_redis = as_beftax[['year']]

for i in range(len(xquintiles)):
    income_col = 'i' + xquintiles[i]
    if income_col in as_beftax.columns:
        as_quintiles_redis[income_col] = as_beftax[income_col]
    else:
        print(f"Income column '{income_col}' not found in AS data.")
        continue
    
    add_cols = [col + xquintiles[i] + '_Sum' for col in xredisadd if col + xquintiles[i] + '_Sum' in as_beftax.columns]
    sub_cols = [col + xquintiles[i] + '_Sum' for col in xredissub if col + xquintiles[i] + '_Sum' in as_beftax.columns]
    
    print(f"Adding columns for quintile {xquintile_names[i]}: {add_cols}")
    print(f"Subtracting columns for quintile {xquintile_names[i]}: {sub_cols}")
    
    if add_cols and sub_cols:
        x1 = as_beftax[add_cols].sum(axis=1)
        x2 = as_beftax[sub_cols].sum(axis=1)
        # Compute redistribution amount
        as_quintiles_redis['redisamt' + xquintile_names[i]] = (x1 - x2) / 1e6
        # Compute redistribution rate as a percentage of income
        as_quintiles_redis['redisrate' + xquintile_names[i]] = 100 * (x1 - x2) / as_beftax[income_col]
    else:
        print(f"Data columns for quintile '{xquintile_names[i]}' are incomplete.")

#%% Plot first figure (A&S vs PSZ)

# First Figure: AS data and PSZ data (with AS income groups)
fig1, axs1 = plt.subplots(1, 2, figsize=(10, 5))
fig1.suptitle('Figure 3: Tax & transfer rates, PSZ (1962-2019) v. AS (1966-2019)')
# AS data (left subplot)
for percname in aspercnames:
    if 'redisrate'+percname in as_redis.columns:
        axs1[0].plot(as_redis['year'], as_redis['redisrate'+percname], label=percname)

#axs1[0].set_xlabel('Year')
axs1[0].set_ylabel('Tax & Transfer (%)')
axs1[0].set_title('Auten & Splinter')
#axs1[0].legend()
# Place legend in _figure_ which puts it below both subplots
# Put it here (after the first subplot) so it uses only the labels from first subplot
# See https://stackoverflow.com/questions/4700614/how-to-put-the-legend-outside-the-plot
fig1.legend(loc='upper center', bbox_to_anchor=(0.5, 0.02),
          fancybox=False, shadow=False, ncol=4,fontsize=11)


axs1[0].set_ylim(ymin, ymax)
axs1[0].set_xlim(1960, 2020)
axs1[0].grid(axis='y', alpha=0.25)
axs1[0].grid(axis='x', alpha=0)


# PSZ data (right subplot) with same income groups as AS
for percname in pszpercnames:
    if percname in psz_merged.columns:
        axs1[1].plot(psz_merged['year'], psz_merged[percname], label=percname)
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
#axs1[1].set_xlabel('Year')
axs1[1].set_ylabel('')
axs1[1].set_title('Piketty, Saez, Zucman')
#axs1[1].legend()
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
#plt.savefig('figures/figure3_output.pdf',bbox_inches="tight") 
plt.show()
plt.close()


#%% Load and process Auten & Splinter data for quintiles (for comparison with CBO)
# -----------------------------------------
# Load and process Auten & Splinter (AS) data
# -----------------------------------------
rows_pretax = range(4, 65)
as_beftax = pd.read_excel(file_path + "AutenSplinter-IncomeIneq_2024.xlsx", 
                          sheet_name="Output2", skiprows=rows_pretax[0], nrows=len(rows_pretax))

if 'Year' in as_beftax.columns:
    as_beftax.rename(columns={'Year': 'year'}, inplace=True)

# Define quintile identifiers and names
xquintiles = ['q1noneg', 'q2', 'q3', 'q4', 'q5']
xquintile_names = ['Quintile1', 'Quintile2', 'Quintile3', 'Quintile4', 'Quintile5']

xredisadd = ['f', 'st', 'x', 'p', 'o', 'wt', 'es']
xredissub = ['s', 'mc', 'ca', 'nc']

# Initialize DataFrame to store the AS quintile results
as_quintiles_redis = as_beftax[['year']]

# Check for quintile columns
print("Available columns in AS data:", as_beftax.columns)

# Loop over each quintile to compute redistribution rates
for i in range(len(xquintiles)):
    quintile = xquintiles[i]
    quintile_name = xquintile_names[i]
    
    # Income for the quintile
    income_col = quintile
    if income_col in as_beftax.columns:
        as_quintiles_redis[quintile_name + '_Income'] = as_beftax[income_col]
    else:
        print(f"Income column '{income_col}' not found in AS data.")
        continue

    # Taxes and transfers: sum of additions minus subtractions
    add_cols = [col + f'q{i + 1}_Sum' for col in xredisadd if col + f'q{i + 1}_Sum' in as_beftax.columns]
    sub_cols = [col + f'q{i + 1}_Sum' for col in xredissub if col + f'q{i + 1}_Sum' in as_beftax.columns]

    print(f"Adding columns for {quintile_name}: {add_cols}")
    print(f"Subtracting columns for {quintile_name}: {sub_cols}")

    if add_cols and sub_cols:
        total_add = as_beftax[add_cols].sum(axis=1)
        total_sub = as_beftax[sub_cols].sum(axis=1)

        # Compute redistribution amount and rate
        as_quintiles_redis['redisamt_' + quintile_name] = (total_add - total_sub) / 1e6  # Redistribution amount in millions
        as_quintiles_redis['redisrate_' + quintile_name] = 100 * (total_add - total_sub) / as_beftax[income_col]  # Redistribution rate as percentage of income
    else:
        print(f"Data columns for quintile '{quintile_name}' are incomplete.")

#%% Load and process CBO data for second plot

#%% Load CBO data
# -----------------------------------------
# Load and process CBO data for Second Plot
# -----------------------------------------
cbo_avginc_full_rankbeftax = pd.read_csv(cbofile_path + "households_ranked_by_inc_before_trans_tax_table_03_average_household_income_1979_2019.csv")
cbo_avginc_full_rankmkt = pd.read_csv(cbofile_path + "households_ranked_by_market_inc_table_03_average_household_income_1979_2019.csv")

required_columns = ['year', 'income_group', 'inc_before_transfers_taxes', 'inc_after_transfers_taxes', 'market_income']
cbo_avginc_full_rankbeftax = cbo_avginc_full_rankbeftax[required_columns].dropna()

def aggregate_cbo_data(df, income_column):
    return df.groupby(['year', 'income_group'])[income_column].mean().unstack()

# Create aggregations for market, before-tax, and after-tax income all ranked by before-tax income
cbo_mktinc = aggregate_cbo_data(cbo_avginc_full_rankbeftax, 'market_income')
cbo_before_tax = aggregate_cbo_data(cbo_avginc_full_rankbeftax, 'inc_before_transfers_taxes')
cbo_after_tax = aggregate_cbo_data(cbo_avginc_full_rankbeftax, 'inc_after_transfers_taxes')

# Calculate CBO redistribution rates - going from market income to after-tax income
if not cbo_mktinc.empty and not cbo_after_tax.empty:
    cbo_redistribution = 100 * (1 - cbo_after_tax / cbo_mktinc)
else:
    cbo_redistribution = pd.DataFrame()

#%% Plotting AS Quintiles vs CBO Quintiles (Second Plot)
# -----------------------------------------
# Plotting AS Quintiles vs. CBO Quintiles (Second Plot)
# -----------------------------------------
fig2, axs2 = plt.subplots(1, 2, figsize=(10,5))

fig2.suptitle('Figure 4: Tax & transfer rates: AS (1966-2019) v. CBO (1979-2019)')

# AS Quintiles (left subplot)
for i, quintile_name in enumerate(xquintile_names):
    rate_col = 'redisrate_' + quintile_name
    if rate_col in as_quintiles_redis.columns:
        axs2[0].plot(as_quintiles_redis['year'], as_quintiles_redis[rate_col] / 1e6, label=quintile_name)

#axs2[0].set_xlabel('Year')
axs2[0].set_ylabel('Tax & Transfer (%)')
axs2[0].set_title('Auten & Splinter')
#axs2[0].legend(frameon=False)
# Place legend in _figure_ which puts it below both subplots
# Put it here (after the first subplot) so it uses only the labels from first subplot
# See https://stackoverflow.com/questions/4700614/how-to-put-the-legend-outside-the-plot
fig2.legend(loc='upper center', bbox_to_anchor=(0.5, 0.02),
          fancybox=False, shadow=False, ncol=5,fontsize=11)
axs2[0].set_ylim(-175, 50)
axs2[0].set_xlim(1960, 2020)
axs2[0].grid(axis='y', alpha=0.25)
axs2[0].grid(axis='x', alpha=0)

# CBO Quintiles (right subplot)
quintile_columns_cbo = ['lowest_quintile', 'second_quintile', 'middle_quintile', 'fourth_quintile', 'highest_quintile']
for group, color in zip(quintile_columns_cbo, ['blue', 'red', 'black', 'green', 'orange']):
    if group in cbo_redistribution.columns:
        axs2[1].plot(cbo_redistribution.index, cbo_redistribution[group], label=f'CBO {group.replace("_", " ").title()}')#, color=color)

#axs2[1].set_xlabel('Year')
axs2[1].set_ylabel('')
axs2[1].set_title('Congressional Budget Office')
#axs2[1].legend(frameon=False)#,loc='lower center',ncol=5)
axs2[1].set_ylim(-175, 50)
axs2[1].set_xlim(1960, 2020)
axs2[1].grid(axis='y', alpha=0.25)
axs2[1].grid(axis='x', alpha=0)
axs2[1].axes.yaxis.set_ticklabels([])
axs2[1].spines[['left']].set_visible(False)


# Adjust layout for the second figure
plt.tight_layout()
# totally silly, but need 'bbox_inches='tight'' to force legend to be put into figure
# See https://stackoverflow.com/questions/4700614/how-to-put-the-legend-outside-the-plot
#plt.savefig('figures/figure4_output.pdf',bbox_inches='tight')
plt.show()
plt.close()
