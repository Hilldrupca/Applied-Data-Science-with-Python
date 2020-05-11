import pandas as pd
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



__author__ = 'Chris Hilldrup'



# NOTE: Follow code provided by Coursera
df = pd.read_csv(sys.path[-1] + '/Data/olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(') # split the index by '('

df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')



"""
Which country has won the most gold medals in summer games?
This function should return a single string value.
"""
def answer_one():
    return df['Gold'].idxmax()



"""
Which country had the biggest difference between their summer and winter gold medal counts?
This function should return a single string value.
"""
def answer_two():
    series = pd.Series(df['Gold'] - df['Gold.1'], index=df.index)
    return series.idxmax()



"""
Which country has the biggest difference between their summer gold medal counts and winter gold medal counts  relative to their total gold medal count?

    (Summer Gold - Winter Gold) / Total Gold

Only include countries that have won at least 1 gold in both summer and winter.
This function should return a single string value.
"""
def answer_three():
    masked = df[((df['Gold'] > 0) & (df['Gold.1'] > 0))]
    diffratio = (masked['Gold'] - masked['Gold.1'])/masked['Gold.2']
    return diffratio.idxmax()



"""
Write a function that creates a Series called "Points" which is a weighted value where each gold medal (Gold.2)  counts for 3 points, silver medals (Silver.2) for 2 points, and bronze medals (Bronze.2) for 1 point. The function should return only the column (a Series object) which you created, with the country names as indices.

This function should return a Series named Points of length 146
"""
def answer_four():
    return pd.Series(df['Gold.2']*3 + df['Silver.2']*2 + df['Bronze.2'], index=df.index)



census_df = pd.read_csv(sys.path[-1] + '/Data/census.csv')



"""
Which state has the most counties in it? (hint: consider the sumlevel key carefully! You'll need this for future questions too...)

This function should return a single string value.
"""
def answer_five():
    #Boolean mask ['SUMLEVL'] that doesn't correspond to an actual ['CTYNAME']
    masked = census_df[(census_df['SUMLEV'] > 40)]
    masked = masked.set_index(['STNAME'])
    
    maxcounty = 0
    for x in set(masked.index):
        if maxcounty == 0:
            maxcounty = x
        if len(masked.loc[x]) > len(masked.loc[maxcounty]):
            # set maxcount to state with higher number of counties
            maxcounty = x
            
    return maxcounty



"""
Only looking at the three most populous counties for each state, what are the three most populous states (in order of highest population to lowest population)? Use CENSUS2010POP.

This function should return a list of string values.
"""
def answer_six():
    copy = census_df[(census_df['SUMLEV'] > 40)]
    copy.set_index('STNAME', inplace=True)
    copy = copy['CENSUS2010POP']
    topthree = []
    for x in set(copy.keys()):
        toptotal = copy.loc[x]
        
        if isinstance(toptotal, pd.core.series.Series):
            toptotal = toptotal.sort_values(ascending=False)[:3]

        toptotal = toptotal.sum()
        
        if len(topthree) < 3:
            topthree.append([toptotal,x])
            continue
        
        #Sort so more populous states are at bottom of stack
        topthree.sort(reverse=True)
        
        if min(topthree)[0] < toptotal:
            topthree.pop()
            topthree.append([toptotal,x])
                            
    states = [x[1] for x in topthree]        
    return states



"""
Which county has had the largest absolute change in population within the period 2010-2015? (Hint: population values are stored in columns POPESTIMATE2010 through POPESTIMATE2015, you need to consider all six columns.)

e.g. If County Population in the 5 year period is 100, 120, 80, 105, 100, 130, then its largest change in the period would be |130-80| = 50.

This function should return a single string value.
"""
def answer_seven():
    masked = census_df[(census_df['SUMLEV'] > 40)]
    masked.set_index(['STNAME','CTYNAME'], inplace=True)
    masked = masked[['POPESTIMATE2010','POPESTIMATE2011','POPESTIMATE2012',
                    'POPESTIMATE2013','POPESTIMATE2014','POPESTIMATE2015']]
    topchange = (0,0)
    for x,y in masked.index:
        county = masked.loc[(x,y)]
        high = county.max()
        low = county.min()
        diff = high - low
        if topchange[0] < diff:
            topchange = (diff, y)
    
    return topchange[1]



"""
In this datafile, the United States is broken up into four regions using the "REGION" column.

Create a query that finds the counties that belong to regions 1 or 2, whose name starts with 'Washington', and whose POPESTIMATE2015 was greater than their POPESTIMATE 2014.

This function should return a 5x2 DataFrame with the columns = ['STNAME', 'CTYNAME'] and the same index ID as the census_df (sorted ascending by index).
"""
def answer_eight():
    masked = census_df[(census_df['SUMLEV'] > 40)]
    masked = masked[(masked['REGION'] < 3)]
    masked = masked[(masked['REGION'] > 0)]
    masked = masked[(masked['CTYNAME'].str.startswith('Washington'))]
    masked = masked[(masked['POPESTIMATE2015'] > masked['POPESTIMATE2014'])]
    masked = masked[['STNAME','CTYNAME']]
    return masked

