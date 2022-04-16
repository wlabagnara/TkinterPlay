""" 
    Continuous real-time (animated) data generating method/thread!

    references:
        https://www.youtube.com/watch?v=Ercd-Ip5PfQ

    Note: See partner file 'matplotlibMonitorRealTime.py' used in demo.
        
"""

def data_gen():
    """ 
        Simulate continuous (animated) data - by writing in real-time to a csv file
        
        Needs to run 'externally' or as a thread to keep writing to the csv file
            so that the other routine is reading and plotting the 'animated' data.

        If you want to run this method externally, copy to 'data_gen.py' and
        run as
        
        > python data_gen.py

    """
    import csv
    import random
    import time as t

    x_value = 0
    total_1 = 1000
    total_2 = 1000
    fieldnames = ["x_value", "total_1", "total_2"]
    
    with open('data.csv', 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()

    while True:
        with open('data.csv', 'a') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            info = {
                "x_value": x_value,
                "total_1": total_1,
                "total_2": total_2
            }
            csv_writer.writerow(info)
            print(x_value, total_1, total_2)
            x_value += 1
            total_1 = total_1 + random.randint(-6, 8)
            total_2 = total_2 + random.randint(-5, 6)
        t.sleep(1)


# invoke the method ... it has infinite loop!
data_gen()
