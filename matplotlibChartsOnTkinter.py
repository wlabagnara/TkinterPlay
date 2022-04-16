"""
    Embedding Bar, Line and Scatter charts in tkinter GUI

    references:
        https://datatofish.com/matplotlib-charts-tkinter-gui/
        https://matplotlib.org/stable/plot_types/index.html


"""

import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from pandas import DataFrame

import numpy as np

# create some data
data1 = {'Country': ['US','CA','GER','UK','FR'],
         'GDP_Per_Capita': [45000,42000,52000,49000,47000]
        }

df1 = DataFrame(data1,columns=['Country','GDP_Per_Capita'])
print (df1)

data2 = {'Year': [1920,1930,1940,1950,1960,1970,1980,1990,2000,2010],
         'Unemployment_Rate': [9.8,12,8,7.2,6.9,7,6.5,6.2,5.5,6.3]
        }  
df2 = DataFrame(data2,columns=['Year','Unemployment_Rate'])
print (df2)

data3 = {'Interest_Rate': [5,5.5,6,5.5,5.25,6.5,7,8,7.5,8.5],
         'Stock_Index_Price': [1500,1520,1525,1523,1515,1540,1545,1560,1555,1565]
        }
df3 = DataFrame(data3,columns=['Interest_Rate','Stock_Index_Price'])
print (df3)


# BAR chart
def draw_bar_chart(df_in):    
    fig1 = plt.figure(figsize=(6,5), dpi=100)
    ax1 = fig1.add_subplot(111)

    bar1 = FigureCanvasTkAgg(fig1, root)                                # <=== Tkinter hooks!
    bar1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)               # <===   Display directly with 'pack()'

    df1 = df_in[['Country','GDP_Per_Capita']].groupby('Country').sum()
    df1.plot(kind='bar', legend=True, ax=ax1)
    ax1.set_title('Country vs GDP per Capita')

# Line chart
def draw_line_chart(df_in):
    figure2 = plt.Figure(figsize=(5,4), dpi=100)
    ax2 = figure2.add_subplot(111)

    line2 = FigureCanvasTkAgg(figure2, root)                                     
    line2.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

    df2 = df_in[['Year','Unemployment_Rate']].groupby('Year').sum()
    df2.plot(kind='line', legend=True, ax=ax2, color='r',marker='o', fontsize=10)
    ax2.set_title('Year Vs. Unemployment Rate')

# Scatter chart
def draw_scatter_chart(df_in):
    figure3 = plt.Figure(figsize=(5,4), dpi=100)
    ax3 = figure3.add_subplot(111)
    ax3.scatter(df_in['Interest_Rate'],df_in['Stock_Index_Price'], color = 'g')

    scatter3 = FigureCanvasTkAgg(figure3, root) 
    scatter3.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

    ax3.legend(['Stock_Index_Price']) 
    ax3.set_xlabel('Interest Rate')
    ax3.set_title('Interest Rate Vs. Stock Index Price')

def display_charts():
    # display plots directly on GUI
    draw_bar_chart(df1)
    draw_line_chart(df2)
    draw_scatter_chart(df3)

def draw_histogram():
    # fake data
    house_prices = np.random.normal(200000, 25000, 5000) # normal distribution with: average, standard deviation, number of data points
    # histogram
    plt.hist(house_prices, 200) # data, number of bins - see matplot url reference above for api parameters
    # plt.pie(house_prices ) # for laughs...
    # plt.polar(house_prices ) 
    plt.show()

def display_histogram_via_btn():
    root.geometry("600x800")
    # display plot from gui via button click
    btn1 = tk.Button(root, text="GRAPH RANDOM DATA?", command=draw_histogram)
    btn1.pack()

# add charts to the GUI

root = tk.Tk()

display_charts() # demo 1
# display_histogram_via_btn() # demo 2


root.mainloop()


