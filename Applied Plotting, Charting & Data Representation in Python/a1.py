"""
Before working on this assignment please read these instructions fully. In the submission area, you will notice that you can click the link to Preview the Grading for each step of the assignment. This is the criteria that will be used for peer grading. Please familiarize yourself with the criteria before beginning the assignment.

An NOAA dataset has been stored in the file data/C2A2_data/BinnedCsvs_d400/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv. This is the dataset to use for this assignment. Note: The data for this assignment comes from a subset of The National Centers for Environmental Information (NCEI) Daily Global Historical Climatology Network (GHCN-Daily). The GHCN-Daily is comprised of daily climate records from thousands of land surface stations across the globe.

Each row in the assignment datafile corresponds to a single observation.

The following variables are provided to you:

    id : station identification code
    date : date in YYYY-MM-DD format (e.g. 2012-01-24 = January 24, 2012)
    element : indicator of element type
        TMAX : Maximum temperature (tenths of degrees C)
        TMIN : Minimum temperature (tenths of degrees C)
    value : data value for element (tenths of degrees C)

For this assignment, you must:

    Read the documentation and familiarize yourself with the dataset, then write some python code which returns a line graph of the record high and record low temperatures by day of the year over the period 2005-2014. The area between the record high and record low temperatures for each day should be shaded.
    Overlay a scatter of the 2015 data for any points (highs and lows) for which the ten year record (2005-2014) record high or record low was broken in 2015.
    Watch out for leap days (i.e. February 29th), it is reasonable to remove these points from the dataset for the purpose of this visualization.
    Make the visual nice! Leverage principles from the first module in this course when developing your solution. Consider issues such as legends, labels, and chart junk.

The data you have been given is near Ann Arbor, Michigan, United States.
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pandas as pd
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



df = pd.read_csv(sys.path[-1] + '/Data/fb441e62df2d58994928907a91895ec62c2c42e6cd075c2700843b89.csv')
# Convert to degrees C from tenths of degrees C
df['Data_Value'] /= 10
df['Date'] = df['Date'].astype('Datetime64')
df.sort_values(by='Date',axis=0, ascending=True, inplace=True)

# Mask February 29th
df.mask((df['Date'].dt.month == 2) & (df['Date'].dt.day == 29), inplace=True)
df.dropna(inplace=True)

daterange = pd.date_range('2015-01-01','2015-12-31')
daysinyear = pd.DataFrame(index=daterange.strftime('%m-%d'),
                          columns=['RecordLow','RecordHigh','2015Low','2015High'])

pre2015 = df[df['Date'] < np.datetime64('2015-01-01')]

# Get 2004-2014 record highs and lows
for x,y in pre2015.groupby(by=pre2015['Date'].dt.strftime('%m-%d')):
    low = y[y['Element'] == 'TMIN']['Data_Value'].min()
    high = y[y['Element'] == 'TMAX']['Data_Value'].max()
    daysinyear.loc[x]['RecordLow'] = low
    daysinyear.loc[x]['RecordHigh'] = high
    
data2015 = df[df['Date'] > np.datetime64('2014-12-31')]

# Get 2015 high and lows that exceed 2004-2014
for x,y in data2015.groupby(by=data2015['Date'].dt.strftime('%m-%d')):
    low = y[y['Element'] == 'TMIN']['Data_Value'].min()
    high = y[y['Element'] == 'TMAX']['Data_Value'].max()
    
    if daysinyear.loc[x]['RecordLow'] > low:
        daysinyear.loc[x]['2015Low'] = low
        
    if daysinyear.loc[x]['RecordHigh'] < high:
        daysinyear.loc[x]['2015High'] = high
        
fig,ax = plt.subplots()
fig.set_size_inches(16,9)

# 2004-2014 data line plot
linelow = plt.plot(daterange, daysinyear['RecordLow'],
                   color='k', linewidth=.5, alpha=.5)
linehigh = plt.plot(daterange, daysinyear['RecordHigh'],
                    color='k', linewidth=.5, alpha=.5)
plt.fill_between(list(daterange), list(daysinyear['RecordLow']),
                 list(daysinyear['RecordHigh']), color='lightslategray',
                 label='2004-2014 Record High and Low Range', alpha=.2)

# 2015 data scatter plot
plt.scatter(daterange, daysinyear['2015High'], label='2015 Record High',
            color='#ff7f0e',marker='^', edgecolor='black', linewidths=0.5)
plt.scatter(daterange, daysinyear['2015Low'], label='2015 Record Low',
            color='cyan', marker='v', edgecolor='black', linewidths=0.5)

# Format x-axis ticks and their labels
ax.set_xticklabels(daterange, rotation=-45, ha='left')
ax.xaxis.set_major_locator(mdates.MonthLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%b'))
ax.xaxis.get_major_ticks()[-1].set_visible(False)

plt.grid(True,axis='y', alpha=.4)
plt.legend()
plt.title('Record High and Low Temperatures from 2015\nby Day of Year vs Previous Ten Years')
ax.set_ylabel('Temperature ($^\circ$C)')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

#plt.show()
plt.savefig('2004-2015 Temperature Records.png',dpi=100)
