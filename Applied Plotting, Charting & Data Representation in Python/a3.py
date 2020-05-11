"""
This assignment requires that you to find at least two datasets on the web which are related, and that you visualize these datasets to answer a question with the broad topic of sports or athletics (see below) for the region of Ann Arbor, Michigan, United States, or United States more broadly.


Choice:

The goal is to see trends (if any) of rising temperatures on crop yields.
Crop yield is represented in tonnes per hectare, and is plotted against the
temperature increase over the previous year from 1961-2018. Data sets/pots
represent the world, and countries divided into economic groups.

Crop data comes from http://www.fao.org/faostat/en/#data/QC
Temperature data comes from http://www.fao.org/faostat/en/#data/ET
"""
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.lines as mlines
import pandas as pd
import sys, os
from scipy.stats import ttest_ind
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



__author__ = 'Chris Hilldrup'



# Continents
reg_contin = {'Africa': 'Africa',
             'Asia': 'Asia',
             'Australia and New Zealand': 'Australia',
             'Europe': 'Europe',
             'Central America': 'North America',
             'Northern America':'North America',
             'Caribbean': 'North America',
             'South America': 'South America'}

# Economic Regions
reg_economic = {'Northern America': 'Developed Region',
               'Europe': 'Developed Region',
               'Japan': 'Developed Region',
               'Australia and New Zealand': 'Developed Region',
               'Israel': 'Developed Region',
               'Botswana': 'Developed Region',
               'Lesotho': 'Developed Region',
               'Namibia': 'Developed Region',
               'South Africa': 'Developed Region',
               'Eswatini': 'Developed Region',
               'Slovenia': 'Developed Region',
               'Africa': 'Developing Region',
               'Caribbean': 'Developing Region',
               'Central America': 'Developing Region',
               'South America': 'Developing Region',
               'Asia': 'Developing Region',
               'Oceania': 'Developing Region',
               'Azerbaijan': 'Transition Country',
               'Belarus': 'Transition Country',
               'Kazakhstan': 'Transition Country',
               'Kyrgyzstan': 'Transition Country',
               'Armenia': 'Transition Country',
               'Moldova': 'Transition Country',
               'Russia': 'Transition Country',
               'Tajikistan': 'Transition Country',
               'Uzbekistan': 'Transition Country',
               'Turkmenistan': 'Transition Country',
               'Ukraine': 'Transition Country',
               'Albania': 'Transition Country',
               'Bosnia and Herzegovina': 'Transition Country',
               'Croatia': 'Transition Country',
               'Serbia and Montenegro': 'Transition Country',
               'Montenegro': 'Transition Country',
               'Serbia': 'Transition Country',
               'North Macedonia': 'Transition Country',
               'Land Locked Developing Countries': 'Developing Countries',
               'Small Island Developing States': 'Developing Countries',
               'Least Developed Countries': 'Developing Countries'}

def dataframe_ttest(df=None, axis=None):
    '''
    Calculate p-value between two series and apply values to axis. Also
    determines if variance is equal or not.
    
    Parameters:
        df - DataFrame object with values to be compared. Currently requires
             columns labeled 'Value_x' and 'Value_y'.
        axis - The axis object to apply the p-value to.
    '''
    if df is None or axis is None:
        return
    
    varcrop = df['Value_x'].var()
    vartemp = df['Value_y'].var()
    varequal = (varcrop == vartemp)
    p = ttest_ind(a=df['Value_x'], b=df['Value_y'], equal_var=varequal)
    axis.text(0.01, 0.92,
              'p = ' + str(p[1]) + '\n' +
              'equal variance - ' +
              str(varequal),
              transform=axis.transAxes,
              fontsize=8)
    
# A list of areas from the above dictionaries
reg_wanted = list(reg_contin.keys())
reg_wanted.extend(list(reg_economic.keys()))
reg_wanted.append('World')

temperature = pd.read_csv(sys.path[-1] + '/Data/Environment_Temperature_change_E_All_Data_(Normalized).zip',
                          usecols=[1,3,5,7,9], encoding='iso-8859-1')

# Filter unwanted timepoints, temeprature statistics, and areas
temperature = temperature[temperature['Months'] == 'Meteorological year']
temperature = temperature[temperature['Element'] == 'Temperature change']
temperature = temperature[temperature['Area'].isin(reg_wanted)]

crops = pd.read_csv(sys.path[-1] + '/Data/Production_Crops_E_All_Data_(Normalized).zip',
                    usecols=[1,3,7,8,9], encoding='iso-8859-1')

# Keep only ha and tonne values
crops = crops[crops['Unit'] != 'hg/ha']

crop_totals = ['Cereals (Rice Milled Eqv)','Cereals, Total','Citrus Fruit, Total',
               'Coarse Grain, Total', 'Fibre Crops Primary','Fruit Primary',
               'Oilcrops', 'Oilcrops, Cake Equivalent','Oilcrops, Oil Equivalent',
               'Pulses, Total','Roots and Tubers, Total', 'Treenuts, Total',
               'Vegetables Primary']

# Filter unwanted areas, and crops
crops = crops[crops['Area'].isin(reg_wanted)]
crops = crops[crops['Item'].isin(crop_totals)]

df = pd.DataFrame()

# Calculate tonnes/ha for each area and year
for x,y in crops.groupby(by=['Area','Year']):
    tonnes = y[y['Unit'] == 'tonnes']
    hect = y[y['Unit'] == 'ha']
    df =df.append({'Area': x[0],
                   'Year': x[1],
                   'Unit': 'tph',
                   'Value': tonnes['Value'].sum()/hect['Value'].sum(),
                  }, 
                   ignore_index=True)
    
df['Year'] = df['Year'].astype(int)
df = df.merge(temperature, on=['Area','Year'])

# World data used for ax1 and ax2
world = df[df['Area'] == 'World']

fig = plt.figure()
gs = fig.add_gridspec(2,4)
ax1 = fig.add_subplot(gs[0,1:3])

# Line plot for crop yield over time for the world
wline = ax1.plot(world['Year'], world['Value_x'], label='Crop Yield')
ax1.set_ylim(0,6)
ax1.set_title('World')
ax1.set_ylabel('Crop Yield (tonnes/hectare)')
ax1.spines['top'].set_visible(False)
ax1.grid(axis='y', alpha=.5)

dataframe_ttest(world, ax1)

# Bar plot for temperature delta for the world
ax2 = ax1.twinx()
wbar = ax2.bar(world['Year'], world['Value_y'], color='lightgray', alpha=.5, label='$\Delta$T')
ax2.set_ylim(-1.0,2.0)
ax2.set_ylabel('$\Delta$T from Previous Year ($^\circ$C)')
ax2.spines['top'].set_visible(False)


economic = df[df['Area'].isin(list(reg_economic.keys()))]
economic.set_index('Area', inplace=True)

subax = [] # Container for second row plots 

# Group counties into economic statues
for x,y in economic.groupby(reg_economic):
    # Aggregate multiple entries for years 1961-2018 in each group
    s = y.groupby('Year').mean()
    
    bottomax = fig.add_subplot(gs[1,len(subax)])
                                  
    # Line plots of economic country groups for crop yield over time
    bottomax.plot(s.index, s['Value_x'], label='Crop Yield')
    bottomax.spines['top'].set_visible(False)
    bottomax.spines['right'].set_visible(False)
    bottomax.set_ylim(0,6)
    bottomax.set_title(x)
    
    for x in range(1,7):
        bottomax.axhline(x, color='black', linewidth=1, alpha=.1)
    
    if len(subax) == 0:
        bottomax.set_ylabel('Crop Yield (tonnes/hectare)')
    
    if len(subax) > 0:
        bottomax.spines['left'].set_visible(False)
        bottomax.yaxis.set_major_locator(plt.NullLocator())
    
    bottomax.spines['top'].set_visible(False)
    
    # Temperature delta for each economic group plot
    bottomax2 = bottomax.twinx()
    bottomax2.bar(s.index, s['Value_y'], color='lightgray', alpha=.5, label='$\Delta$T')
    bottomax2.spines['top'].set_visible(False)
    bottomax2.spines['left'].set_visible(False)
    bottomax2.set_ylim(-1.0,2.0)
    
    if len(subax) < 3:
        bottomax2.spines['right'].set_visible(False)
        bottomax2.yaxis.set_major_locator(plt.NullLocator())
    
    if len(subax) == 3:
        bottomax2.set_ylabel('$\Delta$T from Previous Year ($^\circ$C)')
    
    dataframe_ttest(y,bottomax)
    
    subax.append([bottomax, bottomax2])
    

fig.suptitle('Does Crop Yield$^1$ change as Surface Temperatures$^2$ Rise for\n' +
             'the World and Economic Country Groups$^3$ from 1961-2018')

# Proxy artist for line plot legend entry
blueline = mlines.Line2D([], [], color='C0')
fig.legend((blueline, wbar),('Crop Yield','$\Delta$T'))

plt.figtext(0.005, 0.9,
            '$^1$ Crop data source - http:/www.fao.org/faostat/en/#data/QC\n' + 
            '$^2$ Temperature data source - http:/www.fao.org/faostat/en/#data/ET\n' +
            '$^3$ Economic Country Groups according to UN M49 (2009)\n' + 
            '- This is a general analysis. Underlying or additional factors\nare not considered.',
            horizontalalignment='left')

plt.show()
