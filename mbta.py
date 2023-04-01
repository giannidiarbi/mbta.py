'''
    Gianni Diarbi
    DS2000
    Spring 2023
    Starter code for HW5 - a main and a couple of baisc functions.
    
    Your job is to write the rest of the functions main relies on! 
    
'''

import csv
import matplotlib.pyplot as plt

MBTA_FILE = "mbta_data.csv"
LINE_COL = 3
TOTAL_ON = 12
TOTAL_OFF = 13
TIME_OF_DAY = 8

def read_file(filename):
    ''' Function: read_file
        Parameters: filename (string) for a CSV file
        Returns: 2d list of what the file contains
        Does: Reads every line of the file, except the header,
              and stored in a 2d list which is returned at the end
    '''
    data = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter = ",")
        next(reader)
        for row in reader:
            data.append(row)
    return data

def get_col(data, col):
    ''' Function: get_col
        Parameters 2d list of anything, a column number (int)
        Returns: one column of the 2d list, turned into a list of its own
        Does: Loops over the 2d list, and for each sublist, appends
              a value at the given location onto a new list
    '''
    lst = []
    for row in data:
        lst.append(row[col])
    return lst

def riders_per_line(data, mbta_line, color_col, number_col):
    ''' Function: riders_per_line
        Parameters: 2d list of data strings, string for MBTA line of interest, int 
        for column number of color, int for column number of number of riders
        Returns: a float value representing the avg number of riders getting 
        on line of interest
        Does: Scans 2D list for MBTA line of interest. If found, add line's
        number of riders to the total amount. Determine and return the avg
        number of riders.
    '''
    total_riders = 0
    number_rows = 0
    
    for row in data:
        if mbta_line in row[color_col]:
            total_riders += int(row[number_col])
            number_rows += 1
            
    avg = float(total_riders / number_rows)
    return avg

def split_by_time(data, time_period, time_column):
               
    ''' Function: split_by_line
        Parameters: 2d list of strings in same structure as CSV file
                    String for time period of interest
                    Int for column number of the time_period column
        Returns: Filtered 2d list of strings
        Does: Sorts through 2d list to create a smaller 2d list containing 
        only the items that match the given time period
    '''
    time_lst = []
    for row in data:
        if row[time_column] == time_period:
            time_lst.append(row)
    return time_lst
            
def plot_ridership(riders, labels):
    ''' Function: plot_ridership
        Parameters: List of number of riders per line (ints)
                    List of labels -- MBTA line names (strings)
        Returns: Nothing
        Does: Creates a bar plot using the list of strings for colors and 
        labels, and using the list of ints for bar heights 
    '''
    for i in range(len(riders)):
        plt.bar(labels[i], riders[i], color = labels[i])
        plt.xlabel("MBTA Line")
        plt.ylabel("Number of Riders")
        plt.title("MBTA Average Ridership")
 
def plot_time_ridership(ridership, lines):
   ''' Function: plot_time_ridership 
       Parameters: 2d list of floats, with each sublist representing the 
       ridership of all MBTA lines at a particular time of day
                   Standard list of line names (strings)
       Returns: Nothing
       Does: Creates a line chart, calling the get_col function to
       obtain data from each of the 4 lines. List of strings is used for plot 
       labels and colors.
    '''
   for i in range(len(lines)):
       line = get_col(ridership, i)
       plt.plot(line, label = lines[i], color = lines[i])
       
   plt.title("Ridership on All Lines Over the Day")
   plt.xlabel("Time of Day")
   plt.ylabel("Number of Riders")
   plt.xticks([i for i in range(0, len(ridership), 3)], \
              ["Early Morning", "Mid Day", "Afternoon", "Night"])
   plt.legend()
    
def main():

    # Step One: Gathering data
    # Get the data as a 2d list of ints
    data = read_file(MBTA_FILE)

    # Step Two: Computations 
    # Compute the average number of riders getting on each line
    lines = ["Green", "Blue", "Red", "Orange"]
    ridership = []
  
    for i in range(len(lines)):
        on_riders = riders_per_line(data, lines[i], LINE_COL, TOTAL_ON)
        ridership.append(on_riders)

    # Step Two: Computations
    # Count the average number of total riders at each time of day
    # We can reuse the ridership functions above, but first we
    # split the data into each separate part of day
    ridership_time = []
    for i in range(1, 12):
        time_period = "time_period_{:02d}".format(i)
        time_data = split_by_time(data, time_period, TIME_OF_DAY)
        curr_riders = []
        for j in range(len(lines)):
            riders = riders_per_line(time_data, lines[j], LINE_COL, TOTAL_ON)
            curr_riders.append(riders)
        ridership_time.append(curr_riders)        

    # Step Three: Communicate! 
    # Plot the average number of riders getting on each line
    plot_ridership(ridership, lines)
    plt.show()
    
    # Plot each line's ridership over the day as a line chart
    plot_time_ridership(ridership_time, lines)
    
    # Communicate part 2... print out average ridership per line
    print("Average ridership per line:")
    for i in range(len(lines)):
        print("\t", lines[i], ": ", round(ridership[i]), " avg riders.",
              sep = "")
   

main()  
  
