'''
In this assignment, you'll be working with messy medical data and using regex to extract relevant infromation from the data.

Each line of the dates.txt file corresponds to a medical note. Each note has a date that needs to be extracted, but each date is encoded in one of many formats.

The goal of this assignment is to correctly identify all of the different date variants encoded in this dataset and to properly normalize and sort the dates.

Here is a list of some of the variants you might encounter in this dataset:

    04/20/2009; 04/20/09; 4/20/09; 4/3/09
    Mar-20-2009; Mar 20, 2009; March 20, 2009; Mar. 20, 2009; Mar 20 2009;
    20 Mar 2009; 20 March 2009; 20 Mar. 2009; 20 March, 2009
    Mar 20th, 2009; Mar 21st, 2009; Mar 22nd, 2009
    Feb 2009; Sep 2009; Oct 2010
    6/2008; 12/2009
    2009; 2010

Once you have extracted these date patterns from the text, the next step is to sort them in ascending chronological order accoring to the following rules:

    Assume all dates in xx/xx/xx format are mm/dd/yy
    Assume all dates where year is encoded in only two digits are years from the 1900's (e.g. 1/5/89 is January 5th, 1989)
    If the day is missing (e.g. 9/2009), assume it is the first day of the month (e.g. September 1, 2009).
    If the month is missing (e.g. 2010), assume it is the first of January of that year (e.g. January 1, 2010).
    Watch out for potential typos as this is a raw, real-life derived dataset.

With these rules in mind, find the correct date in each note and return a pandas Series in chronological order of the original Series' indices.

For example if the original series was this:

0    1999
1    2010
2    1978
3    2015
4    1985

Your function should return this:

0    2
1    4
2    0
3    1
4    3

Your score will be calculated using Kendall's tau, a correlation measure for ordinal data.

This function should return a Series of length 500 and dtype int.
'''
import pandas as pd
import sys, os



sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



__author__ = 'Chris Hilldrup'



# NOTE: following provided by coursera
doc = []
with open(sys.path[-1] + '/Data/dates.txt') as file:
    for line in file:
        doc.append(line)
        
df = pd.Series(doc)
#df.head(10)



def date_sorter():
    dates = df.str.findall(r'(?:\d+\s)?'
                           +'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
                           +'\w*[,\.]?(?:\s\d+)?,?(?:\s\d+)'
                           +'|'
                           +'(?<!\.)'
                           +'\d?\d[/-]\d?\d[/-](?:[1-2]\d{3}|\d{2})'
                           +'|'
                           +'(?<!\.)'
                           +'\d?\d[/-][1-2]\d{3}'
                           +'|'
                           +'[1-2]\d{3}').apply(' '.join)
    
    dates = dates.str.replace(r'Jan\w*','January')
    dates = dates.str.replace(r'Dec\w*','December')
    
    dates2 = pd.to_datetime(dates)
    
    return pd.Series(dates2.sort_values().index)
