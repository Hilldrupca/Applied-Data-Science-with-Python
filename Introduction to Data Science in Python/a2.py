import pandas as pd
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    

__author__ = 'Chris Hilldrup'



"""
Load the energy data from the file Energy Indicators.xls, which is a list of indicators of energy supply and renewable electricity production from the United Nations for the year 2013, and should be put into a DataFrame with the variable name of energy.

Keep in mind that this is an Excel file, and not a comma separated values file. Also, make sure to exclude the footer and header information from the datafile. The first two columns are unneccessary, so you should get rid of them, and you should change the column labels so that the columns are:

['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']

Convert Energy Supply to gigajoules (there are 1,000,000 gigajoules in a petajoule). For all countries which have missing data (e.g. data with "...") make sure this is reflected as np.NaN values.

Rename the following list of countries (for use in later questions):

"Republic of Korea": "South Korea",
"United States of America": "United States",
"United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
"China, Hong Kong Special Administrative Region": "Hong Kong"

There are also several countries with numbers and/or parenthesis in their name. Be sure to remove these,

e.g.

'Bolivia (Plurinational State of)' should be 'Bolivia',

'Switzerland17' should be 'Switzerland'.


Next, load the GDP data from the file world_bank.csv, which is a csv containing countries' GDP from 1960 to 2015 from World Bank. Call this DataFrame GDP.

Make sure to skip the header, and rename the following list of countries:

"Korea, Rep.": "South Korea", 
"Iran, Islamic Rep.": "Iran",
"Hong Kong SAR, China": "Hong Kong"


Finally, load the Sciamgo Journal and Country Rank data for Energy Engineering and Power Technology from the file scimagojr-3.xlsx, which ranks countries based on their journal contributions in the aforementioned area. Call this DataFrame ScimEn.

Join the three datasets: GDP, Energy, and ScimEn into a new dataset (using the intersection of country names). Use only the last 10 years (2006-2015) of GDP data and only the top 15 countries by Scimagojr 'Rank' (Rank 1 through 15).

The index of this DataFrame should be the name of the country, and the columns should be ['Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015'].

This function should return a DataFrame with 20 columns and 15 entries.
"""
def answer_one():
    # For earlier versions of pandas, usecols uses integers. Later versions accept strings
    energy = pd.read_excel(sys.path[-1] + '/Data/Energy Indicators.xls',header=None, usecols='C:F',
                           skiprows=18,nrows=227)

    energy.rename(columns={2 : 'Country', 3 : 'Energy Supply',
                           4 : 'Energy Supply per Capita', 5 : '% Renewable'},
                           inplace=True)

    energy.replace(to_replace={'Energy Supply':'...','Energy Supply per Capita':'...',
                               '% Renewable':'...'}, value=pd.np.NaN, inplace=True)
    
    # Convert from petajoules to gigajoules
    energy['Energy Supply'] *= 1000000
    
    # Remove numbers and parenthesis from country names
    energy['Country'] = energy['Country'].str.replace('\d+','')
    energy['Country'] = energy['Country'].str.replace(' \(\D+\)','')
    
    # Rename certain countries
    energy.replace(to_replace={'Country':['Republic of Korea','United States of America',
                                          'United Kingdom of Great Britain and Northern Ireland',
                                          'China, Hong Kong Special Administrative Region']},
                    value={'Country':['South Korea','United States','United Kingdom','Hong Kong']},
                    inplace=True)

    GDP = pd.read_csv(sys.path[-1] + '/Data/world_bank.csv', skiprows=4)
    
    # Rename certain countries
    GDP.replace(to_replace={'Country Name':['Korea, Rep.','Iran, Islamic Rep.','Hong Kong SAR, China']},
                value={'Country Name':['South Korea','Iran','Hong Kong']},
                inplace=True)
    
    GDP.rename(columns={'Country Name':'Country'}, inplace=True)
    
    ScimEn = pd.read_excel(sys.path[-1] + '/Data/scimagojr-3.xlsx')
    
    # Merge two dataframes
    result = pd.merge(ScimEn, energy)
    # Merge final dataframe
    result = pd.merge(result,GDP)
    result.set_index('Country', inplace=True)
    result.drop([str(x) for x in range(1960,2006)], axis=1, inplace=True)
    result.drop(['Country Code','Indicator Name','Indicator Code'], axis=1, inplace=True)
    result = result[(result['Rank'] < 16)]

    return result



"""
The previous question joined three datasets then reduced this to just the top 15 entries. When you joined the datasets, but before you reduced this to the top 15 items, how many entries did you lose?

This function should return a single number.
"""
def answer_two():
    # For earlier versions of pandas, usecols uses integers. Later versions accept strings
    energy = pd.read_excel(sys.path[-1] + '/Data/Energy Indicators.xls',header=None, usecols='C:F',
                           skiprows=18,nrows=227)

    energy.rename(columns={2 : 'Country', 3 : 'Energy Supply',
                           4 : 'Energy Supply per Capita', 5 : '% Renewable'},
                           inplace=True)

    energy.replace(to_replace={'Energy Supply':'...','Energy Supply per Capita':'...',
                               '% Renewable':'...'}, value=pd.np.NaN, inplace=True)
    
    # Convert from petajoules to gigajoules
    energy['Energy Supply'] *= 1000000
    
    # Remove numbers and parenthesis from country names
    energy['Country'] = energy['Country'].str.replace('\d+','')
    energy['Country'] = energy['Country'].str.replace(' \(\D+\)','')
    
    # Rename certain countries
    energy.replace(to_replace={'Country':['Republic of Korea','United States of America',
                                          'United Kingdom of Great Britain and Northern Ireland',
                                          'China, Hong Kong Special Administrative Region']},
                    value={'Country':['South Korea','United States','United Kingdom','Hong Kong']},
                    inplace=True)

    GDP = pd.read_csv(sys.path[-1] + '/Data/world_bank.csv', skiprows=4)
    
    # Rename certain countries
    GDP.replace(to_replace={'Country Name':['Korea, Rep.','Iran, Islamic Rep.','Hong Kong SAR, China']},
                value={'Country Name':['South Korea','Iran','Hong Kong']},
                inplace=True)
    
    GDP.rename(columns={'Country Name':'Country'}, inplace=True)
    
    ScimEn = pd.read_excel(sys.path[-1] + '/Data/scimagojr-3.xlsx')
    
    result1 = pd.merge(ScimEn, energy, how='inner', left_on='Country', right_on='Country')
    result1 = pd.merge(result1, GDP, how='inner', left_on='Country', right_on='Country')
    
    result2 = pd.merge(ScimEn, energy, how='outer', left_on='Country', right_on='Country')
    restul2 = pd.merge(result2, GDP, how='outer', left_on='Country', right_on='Country')

    return len(result2) - len(result1)



"""
Answer the following questions in the context of only the top 15 countries by Scimagojr Rank (aka the DataFrame returned by answer_one())

What is the average GDP over the last 10 years for each country? (exclude missing values from this calculation.)

This function should return a Series named avgGDP with 15 countries and their average GDP sorted in descending order.
"""
def answer_three():
    Top15 = answer_one()
    avgGDP = Top15[[str(x) for x in range(2006,2016)]].mean(axis=1)\
                    .sort_values(ascending=False)

    return avgGDP



"""
By how much had the GDP changed over the 10 year span for the country with the 6th largest average GDP?

This function should return a single number.
"""
def answer_four():
    Top15 = answer_one()
    avg = Top15[[str(x) for x in range(2006,2016)]]\
                .mean(axis=1)\
                .sort_values(ascending=False)

    country = avg[avg == avg.iloc[5]].index
    country = Top15.loc[country]
    start = country['2006'].values
    finish = country['2015'].values
    return (finish - start)[0]



"""
What is the mean Energy Supply per Capita?

This function should return a single number.
"""
def answer_five():
    Top15 = answer_one()
    avg = Top15['Energy Supply per Capita'].mean()
    return avg



"""
What country has the maximum % Renewable and what is the percentage?

This function should return a tuple with the name of the country and the percentage.
"""
def answer_six():
    Top15 = answer_one()
    countrypercent = Top15['% Renewable'].max()
    name = Top15[(Top15['% Renewable'] == countrypercent)].index[0]
    return (name, countrypercent)



"""
Create a new column that is the ratio of Self-Citations to Total Citations. What is the maximum value for this new column, and what country has the highest ratio?

This function should return a tuple with the name of the country and the ratio.
"""
def answer_seven():
    Top15 = answer_one()
    Top15['Citation Ratio'] = Top15['Self-citations']/Top15['Citations']
    max_ = Top15['Citation Ratio'].max()
    name = Top15[(Top15['Citation Ratio'] == max_)].index[0]
    return (name, max_)



"""
Create a column that estimates the population using Energy Supply and Energy Supply per capita. What is the third most populous country according to this estimate?

This function should return a single string value.
"""
def answer_eight():
    Top15 = answer_one()
    Top15['Energy Population Estimate'] = Top15['Energy Supply']/Top15['Energy Supply per Capita']
    estimate = Top15['Energy Population Estimate'].sort_values(ascending=False).iloc[2]
    country = Top15[(Top15['Energy Population Estimate'] == estimate)].index[0]
    return country



"""
Create a column that estimates the number of citable documents per person. What is the correlation between the number of citable documents per capita and the energy supply per capita? Use the .corr() method, (Pearson's correlation).

This function should return a single number.
"""
def answer_nine():
    Top15 = answer_one()
    Top15['Energy Population Estimate'] = Top15['Energy Supply']/Top15['Energy Supply per Capita']
    Top15['Citable Documents per Person'] = Top15['Citable documents']/Top15['Energy Population Estimate']
    corr = Top15[['Citable Documents per Person','Energy Supply per Capita']]\
                    .astype(dtype='float64')\
                    .corr(method='pearson')
    
    corr = corr.iloc[0]['Energy Supply per Capita']
    return corr



"""
Create a new column with a 1 if the country's % Renewable value is at or above the median for all countries in the top 15, and a 0 if the country's % Renewable value is below the median.

This function should return a series named HighRenew whose index is the country name sorted in ascending order of rank.
"""
def answer_ten():
    Top15 = answer_one()
    med = Top15['% Renewable'].median()
    Top15['HighRenew'] = Top15['% Renewable'].apply(func=lambda x: 1 if (x >= med) else 0)
    return Top15['HighRenew']



"""
Use the following dictionary to group the Countries by Continent, then create a dateframe that displays the sample size (the number of countries in each continent bin), and the sum, mean, and std deviation for the estimated population of each country.

ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}

This function should return a DataFrame with index named Continent ['Asia', 'Australia', 'Europe', 'North America', 'South America'] and columns ['size', 'sum', 'mean', 'std']
"""
def answer_eleven():
    Top15 = answer_one()
    df = pd.DataFrame(columns=['Continent','size','sum','mean','std'])
    df['Continent'] = ['Asia','Australia','Europe','North America','South America']
    df.set_index('Continent', inplace=True)
    
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    
    Top15['Energy Pop Estimate'] = Top15['Energy Supply']/Top15['Energy Supply per Capita']
    
    for x,y in Top15.groupby(ContinentDict):
        pop = y['Energy Pop Estimate']
        row = [len(y.index), pop.sum(), pop.mean(), pop.std()]
        df.loc[x] = row
    
    return df



"""
Cut % Renewable into 5 bins. Group Top15 by the Continent, as well as these new % Renewable bins. How many countries are in each of these groups?

This function should return a Series with a MultiIndex of Continent, then the bins for % Renewable. Do not include groups with no countries.
"""
def answer_twelve():
    Top15 = answer_one()
    ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}
    
    index = []
    data = []
    Top15['% Renewable Bin'],intervals = pd.cut(Top15['% Renewable'],5, retbins=True, include_lowest=True)

    for x,y in Top15.groupby(ContinentDict):
        for a,b in y.set_index('% Renewable Bin').groupby('% Renewable Bin'):
            index.append((x,a))
            data.append(len(b.index))
    
    index = pd.MultiIndex.from_tuples(index, names=['Continent','% Renewable Bin'])
    
    series = pd.Series(data=data, index=index, name='# Countries')            
    
    return series



"""
Convert the Population Estimate series to a string with thousands separator (using commas). Do not round the results.

e.g. 317615384.61538464 -> 317,615,384.61538464

This function should return a Series PopEst whose index is the country name and whose values are the population estimate string.
"""
def answer_thirteen():
    Top15 = answer_one()
    Top15['Energy Pop Estimate'] = (Top15['Energy Supply']/Top15['Energy Supply per Capita']).astype('float64')
    
    PopEst = Top15['Energy Pop Estimate'].apply(func=lambda x: '{:,}'.format(x))
    return PopEst











