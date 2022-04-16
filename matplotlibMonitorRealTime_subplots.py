""" 
    Matplotlib using subplots!

    references:
        https://www.youtube.com/watch?v=XFZRVnP-MTU

    Notes: 
        Point is to use 'subplots' method versus 'py plots' - very useful
        See partner file 'data_1.csv' used in demo. It contains the data that is plotted.
        
"""

import pandas as pd
from matplotlib import pyplot as plt # this is using 'pyplot' module


plt.style.use('seaborn')

def plot1():
    """ 
        First example using pyplot - no subplots yet!
        Notes:
            - interesting, no instantiation was done, like, plt = Plot()
            - called 'stateful' method (not object oriented) being used
                - can call 'plt.gcf()' and 'plt.gca()' directly...
                - one figure per plot kinda thing...
            - prefer object oriented method, with expected instantiation, like...
                - fig, ax = plt.subplots()
    """
    data = pd.read_csv('data_1.csv')
    ages = data['Age']
    dev_sals = data['All_Devs']
    py_sals = data['Python']
    js_sals = data['JavaScript']

    plt.plot(ages, py_sals, label='Python')
    plt.plot(ages, js_sals, label='JavaScript')

    plt.plot(ages, dev_sals, color='#444444', linestyle='--', label='All Devs')

    plt.legend()
    plt.title('Median Salary (USD) by Age')
    plt.xlabel('Ages')
    plt.ylabel('Median Salary (USD)')

    plt.tight_layout() # gives you 'automatic' padding
    plt.show()


def plot2():
    """ 
        second example, starting with subplots!
        Notes:
            - utilize object oriented method, with expected instantiation, like...
                - fig, ax = plt.subplots()
    """
    data = pd.read_csv('data_1.csv')
    ages = data['Age']
    dev_sals = data['All_Devs']
    py_sals = data['Python']
    js_sals = data['JavaScript']

    fig, ax = plt.subplots() # <=== we are instantiating now

    ax.plot(ages, py_sals, label='Python')                                     # <=== 'plt' changed to 'ax'
    ax.plot(ages, js_sals, label='JavaScript')                                 # <===   similarly
    ax.plot(ages, dev_sals, color='#444444', linestyle='--', label='All Devs') # <===   similarly
    ax.legend()                                                                # <===   similarly

    ax.set_title('Median Salary (USD) by Age') # <=== similarly and requires 'title' to change to 'set_title'
    ax.set_xlabel('Ages')                      # <===    'xlabel' to 'set_xlabel'
    ax.set_ylabel('Median Salary (USD)')       # <===    'ylabel' to 'set_ylabel'

    plt.tight_layout()
    plt.show()

def plot3():
    """ 
        third example, continuing with subplots!
        Notes:
            - useful? -> b/c can have multiple axis
            - need to know how axes are returned so you can 'unpack' them when needed!
            - so just focus on what is returned from our subplots() instantiations!...
    """

    # scenerio 1 - default constructor...
    # fig, ax = plt.subplots() 
    # print(ax) # see single axis sublot -> AxesSubplot(0.125,0.11;0.775x0.77)

    # scenerio 2 - construct with 2 rows and 1 column...
    # fig, ax = plt.subplots(nrows=2, ncols=1) 
    # print(ax) # see a list of two subplots ... [<AxesSubplot:> <AxesSubplot:>]

    # scenerio 3 - construct with 2 rows and 2 columns...
    # fig, ax = plt.subplots(nrows=2, ncols=2) 
    # print(ax) # see a list of four subplots ... note: organized as two sublists in a single list
    #           #  [[<AxesSubplot:> <AxesSubplot:>]
    #           #   [<AxesSubplot:> <AxesSubplot:>]]

    # scenerio 4 - construct with 2 rows and 3 columns...
    # fig, ax = plt.subplots(nrows=2, ncols=3) 
    # print(ax) # see a list of six subplots ... note: still organized as two sublists (but each with 3 items) in a single list
    #           #  [[<AxesSubplot:> <AxesSubplot:> <AxesSubplot:>]
    #           #  [<AxesSubplot:> <AxesSubplot:> <AxesSubplot:>]]

    # now that we know all this...
    # scenerio 5 - we can 'UNPACK' the axes as follows (for the 2 rows by 1 column case)
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1) 
    print(ax1) # see AxesSubplot(0.125,0.53;0.775x0.35) for ax1
    print(ax2) # see AxesSubplot(0.125,0.11;0.775x0.35) for ax2

def plot4():
    """ 
        fourth example, continuing with subplots!
    """
    data = pd.read_csv('data_1.csv')
    ages = data['Age']
    dev_sals = data['All_Devs']
    py_sals = data['Python']
    js_sals = data['JavaScript']

    # fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1) # defaults to ax1/ax2 displaying x ticks across bottom of each plot
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True) # now only x ticks across last plot

    # assign to desired axes ax1/ax2 ...
    #  - think of ax1/ax2 as y-axis variables (dependent on 'age' on the x-axis)...
    #   - 'ax1' as median salary for all developers
    #   - 'ax2' as the median salary for python and javascript developers 
    #          X      Y
    ax1.plot(ages, dev_sals, color='#444444', linestyle='--', label='All Devs') # <== will be on ax1's plot 
    ax2.plot(ages, py_sals, label='Python')                                     # <== will be on ax2's plot
    ax2.plot(ages, js_sals, label='JavaScript')                                 #      also on ax2's plot

    # now create plots for ax1 and ax2 (on a single figure)...
    ax1.legend()
    ax1.set_title('Median Salary (USD) by Age') 
    # ax1.set_xlabel('Ages') # will be displayed for ax2 plot, so remove                      
    ax1.set_ylabel('Median Salary (USD)')       

    ax2.legend()
    # ax2.set_title('Median Salary (USD) by Age') # already displayed for ax1 plot, so remove 
    ax2.set_xlabel('Ages')                      
    ax2.set_ylabel('Median Salary (USD)')        

    plt.tight_layout()
    plt.show()

def plot5():
    """ 
        fifth example, continuing with subplots!
        - breakup single figure with two plots into two seperate figures
    """
    data = pd.read_csv('data_1.csv')
    ages = data['Age']
    dev_sals = data['All_Devs']
    py_sals = data['Python']
    js_sals = data['JavaScript']

    fig1, ax1 = plt.subplots() # now ax1 on its own figure
    fig2, ax2 = plt.subplots() # now ax2 on its own figure

    #          X      Y
    ax1.plot(ages, dev_sals, color='#444444', linestyle='--', label='All Devs') # <== will be on ax1's plot 
    ax2.plot(ages, py_sals, label='Python')                                     # <== will be on ax2's plot
    ax2.plot(ages, js_sals, label='JavaScript')                                 #      also on ax2's plot

    # now create plots for ax1 and ax2 (on a single figure)...
    ax1.legend()
    ax1.set_title('Median Salary (USD) by Age') 
    # ax1.set_xlabel('Ages') # will be displayed for ax2 plot, so remove                      
    ax1.set_ylabel('Median Salary (USD)')       

    ax2.legend()
    # ax2.set_title('Median Salary (USD) by Age') # already displayed for ax1 plot, so remove 
    ax2.set_xlabel('Ages')                      
    ax2.set_ylabel('Median Salary (USD)')        

    plt.tight_layout()
    plt.show()

    # can also save your figures... nice for automation - have script save off the plots!
    fig1.savefig('fig1.png')
    fig2.savefig('fig2.png')

# call your example demo function!...
# plot1() # demo 1
# plot2() # demo 2
# plot3() # demo 3
# plot4() # demo 4
plot5() # demo 5
