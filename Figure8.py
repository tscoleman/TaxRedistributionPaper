##############################################
#                                                         #
# Produces Figure 8 "Share of Transfers for each quintile #
# Using A&S data                                          #
#                                                         #
##############################################


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import warnings
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
plt.rcParams['axes.prop_cycle'] = (cycler(linestyle=["-",":","--","-.", (5, (10, 3)),(0, (3, 5, 1, 5, 1, 5))]) 
                                   + cycler(color=[ '#000000','#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']))
#plt.rcParams['lines.linestyle'] = 'dashed'
plt.grid(axis='x',alpha=.0)
plt.grid(axis='y',alpha=.25)


#%%

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

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore")

# Read the uploaded Excel files
file_path = "C:\\Users\\decla\\Downloads\\"
file_name = 'AutenSplinter-IncomeIneq_2024.xlsx'
file_path = '/Users/tcoleman/tom/Economics/Harris/research/IncomeInequality/AS_PSZdata/'
file_name = 'AutenSplinter-IncomeIneq_2024.xlsx'
file_path = ''

as_file_path = file_path+file_name


# Load the data (same code as for Figure 6)
# It would be better if python had a read_xls function like R, where one could specify rows to read
data_output2 = pd.read_excel(file_path+file_name, sheet_name='Output2')

data_pretax = data_output2.iloc[3:64,2:]   # Read just the rows we want (rows 5:65, with 5 being headers)
                                           # But remember python indexes from zero, so it is python rows 4:64. So why 3??
data_pretax = data_pretax.dropna()
data_pretax.columns = data_pretax.iloc[0]    # Sets columns from headings in Excel sheet
data_pretax = data_pretax.drop(index=data_pretax.iloc[0].name)  # This will drop the 0th row, which were put into column names
data_pretax.set_index('year',drop=False,inplace=True)  # use year as index

# Need this to test for NaN (numpy or math will not work because includes strings)
def isNaN(num):
    return num != num

# Growth, indexed to index year, for before tax income
pctl_graph = ['bottomQ','Q2','Q3','Q4','topQ']
pctl_names = ['Bottom Quintile','Q2','Q3','Q4','Top Quintile']
beftax_pctl = ['q1noneg','q2','q3','q4','q5'] # NB A&S use 'noneg' for bottom quintile, in their sheet C1a-Quin and C7a-Redis

# Now need to sum up transfers, which means combining various columns
# Make list of names for calculating transfers
#   TAXES:
#      f (Col CD ...) 'Federal income tax (less ref. credits)'
#      st (col CL ...) 'State income tax'
#      x (col CT ...) 'Corp tax'
#      p (col DB ...) 'Property taxes'
#      o (col DR ...) 'Other taxes'  
#      wt (col DJ ...) 'Payroll taxes'
#      es (col EH ...) 'Estate taxes' 
#   TRANSFERS
#      s (col BN ...) 'SS+UI benefits'
#      mc (col EX ...) 'Medicare benefits'
#      ca (col FF ...) 'Cash transfers'
#      nc (col FN ...) 'Non-cash transfers'
#  Divided by Pre-tax Income 
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
afttax_pctl = ['q1','q2','q3','q4','q5']
#    xquintilesa = ['q1','q2','q3','q4','q5','5']
#    xquintilesb = ['q1','q2','q3','q4','q5','i5']  
    
# Loop over the desired quintiles, and for each quintile sum up the adds and subs for
# different incomes to go from before-tax to after-transfer&tax
for pctlb, pctla in zip(beftax_pctl,afttax_pctl):
    xlista = [namea+pctla+'_Sum' for namea in xafttaxadd]  # list comprehension to build list of adding transfer incomes
    data_pretax[pctla+'_t'] = (data_pretax[xlista].sum(axis=1))/1000000
# Now calculate transfers as ratio
    data_pretax[pctla+'_ratio'] =  data_pretax[pctla+'_t'] / data_pretax['itot']  # Ratio of transfers to pre-tax income
    data_pretax[pctla+'_share'] =  data_pretax[pctlb] / data_pretax['itot']  # Ratio of transfers to pre-tax income






# Create subplots for both figures
fig, axs = plt.subplots(1, 2, figsize=(14, 6))

# Plot the first figure on the left
for label, pctla in zip(pctl_names,afttax_pctl):
    axs[0].plot(data_pretax['year'],data_pretax[pctla+'_ratio'], label=label, linewidth=1.)
axs[0].set_title("Transfers as Share of National Income",fontsize=16)
#axs[0].set_xlabel("Year")
axs[0].set_ylabel("Percentage")
axs[0].set_ylim(0,0.06)
#axs[0].legend(title="Income Group", loc='lower center', ncol=2)
#axs[0].grid(True)
#axs[0].set_box_aspect(aspect=0.6)
axs[0].grid(axis='y',alpha=0.25)  # Only horizontal gridlines
axs[0].grid(axis='x',alpha=0.)  # Only horizontal gridlines
axs[0].yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:.0%}'))
# Shrink current axis's height by 10% on the bottom
box = axs[0].get_position()
#axs[0].set_position([box.x0, box.y0 + box.height * 0.2,
#                 box.width, box.height * 0.8])

# Put a legend below current axis
axs[0].legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),
          fancybox=True, shadow=True, ncol=5,fontsize=13)

# Plot the second figure on the right
axs[1].plot(data_pretax['year'],data_pretax['q1_ratio'], label='Transfers', linewidth=1.)
axs[1].plot(data_pretax['year'],data_pretax['q1_share'], label='Income Share', linewidth=1.)
axs[1].set_title("Bottom Quintile Transfers vs. Pre-Tax Income Share",fontsize=16)
#axs[1].set_xlabel("Year")
#axs[1].set_ylabel("Percentage")
axs[1].set_ylim(0,0.06)
#axs[1].legend(title="Income Group", loc='lower center', ncol=2)
#axs[1].set_box_aspect(aspect=0.6)
axs[1].grid(axis='y',alpha=0.25)  # Only horizontal gridlines
axs[1].grid(axis='x',alpha=0.)  # Only horizontal gridlines
axs[1].axes.yaxis.set_ticklabels([])
axs[1].spines[['left']].set_visible(False)
#axs[1].yaxis.set_major_formatter(FuncFormatter(lambda y, _: f'{y:.0%}'))
# Shrink current axis's height by 10% on the bottom
box = axs[1].get_position()
#axs[1].set_position([box.x0, box.y0 + box.height * 0.1,
#                 box.width, box.height * 0.5])

# Put a legend below current axis
axs[1].legend(loc='upper center', bbox_to_anchor=(0.5, -0.1),
          fancybox=True, shadow=True, ncol=2,fontsize=13)

'''
# Shrink current axis's height by 10% on the bottom
box = ax.get_position()
ax.set_position([box.x0, box.y0 + box.height * 0.1,
                 box.width, box.height * 0.9])

# Put a legend below current axis
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),
          fancybox=True, shadow=True, ncol=5)
'''

# Set the overall title for the figure
fig.suptitle("Figure 8: Share of transfers for each quintile and for bottom quintile")#, fontsize=14)
#fig.suptitle("Share of transfers for each quintile and for bottom quintile")#, fontsize=14)

# Adjust layout to avoid overlap
plt.tight_layout(rect=[0, 0, 1.2, 1.1])
plt.tight_layout()

file_path = "C:\\Users\\decla\\Downloads\\"
file_path = '/Users/tcoleman/tom/Economics/Harris/research/IncomeInequality/AS_PSZdata/'
file_path = ''

# Save the figure as a PDF
plt.savefig('figures/figure8_Transfers_and_Income_Shares.pdf')

# Show the combined figure
plt.show()





