"""
    Easiest option: Implement the bar coloring as described above - a color scale with only three colors, (e.g. blue, white, and red). Assume the user provides the y axis value of interest as a parameter or variable.

    Harder option: Implement the bar coloring as described in the paper, where the color of the bar is actually based on the amount of data covered (e.g. a gradient ranging from dark blue for the distribution being certainly below this y-axis, to white if the value is certainly contained, to dark red if the value is certainly not contained as the distribution is above the axis).

    Even Harder option: Add interactivity to the above, which allows the user to click on the y axis to set the      value of interest. The bar colors should change with respect to what value the user has selected.

    Hardest option: Allow the user to interactively set a range of y values they are interested in, and recolor based on this (e.g. a y-axis band, see the paper for more details).

    Choice --> Even Harder option
"""
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import numpy as np
import math



np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                   np.random.normal(43000,100000,3650), 
                   np.random.normal(43500,140000,3650), 
                   np.random.normal(48000,70000,3650)], 
                  index=[1992,1993,1994,1995])

fig, ax = plt.subplots()
cmap = mpl.cm.get_cmap('RdBu_r')
plt.colorbar(mpl.cm.ScalarMappable(cmap='RdBu_r'))

def onclick(event):
    # Using clear instead of removing Artists to avoid permanent graph squishing
    # if upper most y levels are clicked
    ax.clear()
    
    # Enable clicking to redraw bar plots with new colors base on clicked y level
    colorbars(event.ydata)

def colorbars(ylevel=None):

    # 0.8 is the default bar width
    width = 0.8

    if ylevel:
        ax.axhline(ylevel,0,1, color='gray')

    # Plot mean bar charts grouped together
    for year in df.index:
        data = df.loc[year]
        count = len(data)
        mean = data.mean()
        std = data.std()
        ci = 1.95*std/math.sqrt(count)
        
        if ylevel:
            # Normalize ylevel with respect to confidence interval
            colorvalue = 1 - (ylevel - mean + ci)/(2*ci)
            ax.bar(width-0.4, mean, color=cmap(colorvalue), yerr=ci, capsize=15)
        else:
            ax.bar(width-0.4, mean, yerr=ci,capsize=15)
            
        width += 0.8

    fig.canvas.mpl_connect('button_press_event',onclick)
    
    ax.set_xticklabels(df.index)
    ax.set_xticks(np.arange(0.4, 3.6, 0.8)) # Align tick marks with bar plots
    ax.set_xlim(-0.05) # Shift bar plots closer to y-axis
    plt.title('Click to Adjust Y Level of Interest\n'
            + 'Click Outside Graph for Standard Bar Chart')


    plt.show()
    #plt.savefig('Interactive Bar Chart')

colorbars(40000)
