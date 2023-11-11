#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
November 4, 2022

A program that reads the data of blue bikes in the last week of September
into a list of dictionaries and analyzes the days, distances, and speeds
of the data. 

Output:
Number of trips ending at Forsyth St at Huntington Ave: 
 {'Friday': 481, 'Saturday': 230, 'Sunday': 219, 'Monday': 250, 'Tuesday': 314, 'Wednesday': 296, 'Thursday': 277}
"""

import math
import matplotlib.pyplot as plt
TRIPS = "trips.csv"
STATIONS = "stations.csv"
EARTH_RADIUS = 3959 # in miles


# question 1: reading the data into list of dictionaries
# - trips: headers are keys (strings); values are corresponding row
# - stations: sep dict that maps station names to GPS coords 



def read_data_dict(filename, type_cast_dict = {}):
    """
    Reads in the data in a given file
    and stores the values in a list of dicts of strings (by default).
    Assumes that commas separate row items in the given file.
    from data utils

    Parameters
    ----------
    filename : string
        name of the file

    type_casts: dict, optional
        type specification for each column in the data
    Returns
    -------
    data : list of dicts
        list of dicts of values for all lines in the file
    """
    file = open(filename, "r")
    data = []
   
    headers = file.readline()
    headers = headers.strip().split(",")
     
    for line in file:
        pieces = line.strip().split(",")
        
        row_dict = {}
        # go through each column and link the value
        # to the appropriate header
        for i in range(len(pieces)):
        
            # {"rotten_tomato": int, "IMDB": float}
            if headers[i] in type_cast_dict:
                cast_func = type_cast_dict[headers[i]]
                row_dict[headers[i]] = cast_func(pieces[i])
            else:
                row_dict[headers[i]] = pieces[i]
                
        data.append(row_dict)
        
    file.close()
    return data


def read_data(filename):
    """
    Reads in the data in a given file
    and stores the values in a list of lists of strings (by default).
    Assumes that commas separate row items in the given file.
    from data utils
    Parameters
    ----------
    filename : string
        name of the file
    skip_header: boolean, optional
        whether or not to skip a header row. Default to False.
    type_casts: list, optional
        type specification for each column in the data
    Returns
    -------
    data : list of lists
        list of lists of values for all lines in the file

    """
    file = open(filename, "r")
    data = {}
    # do we need to skip the first row?
    file.readline()

    for line in file:
        pieces = line.strip().split(",")
        # making the lat and long floats
        pieces[1] = float(pieces[1])
        pieces[2] = float(pieces[2])
        
        names = str(pieces[0])
        coords = [pieces[1], pieces[2]]
        data[names] = coords
        
        

        
        
    file.close()
    return data

        
        

# question 2: calculating the distance and speed of each trip 
def haversine_distance(start, end):
    """
    Calculates the distance in miles between two points on the earth's surface
    described by latitude and longitude.
    from hw7

    Parameters:
        start: list
                list of two floats—latitude and longitude
        end: list
                list of two floats—latitude and longitude
    Return:
        float - distance in miles between the two points
    """
    lat1 = start[0]
    long1 = start[1]
    lat2 = end[0]
    long2 = end[1]
    
    lat1 = math.radians(lat1)
    long1 = math.radians(long1)
    lat2 = math.radians(lat2)
    long2 = math.radians(long2)
    
    delta_lat = lat2 - lat1
    delta_long = long2 - long1
    
    # the earth's radius is a constant value
    a = math.sin(delta_lat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(delta_long / 2)**2
    haversine = EARTH_RADIUS * 2 * math.asin(math.sqrt(a))
    
    return haversine

        
def calculate(trips, stations):
    """
    calculates the distance + speed and adds it to trip     
    
    Parameters
    ----------
    trips : dict
    stations : dict

    Returns
    -------
    None.

    """
    
    for trip_dict in trips: 
     # extracting the column
        start_station = trip_dict['start_station']
        end_station = trip_dict['end_station']
        # making sure both are in stations 
        if start_station in stations and end_station in stations: 
            # distance formula specific for the start and end
            distance = haversine_distance(stations[start_station], stations[end_station])
            # conversions
            duration = float(trip_dict['duration']) / 3600
            
            speed = distance / duration 
            # updating dict
            trip_dict.update({'distance': distance})
            trip_dict.update({'speed': speed})
            
        else:
            # filling in the rest
            trip_dict.update({'distance': None})
            trip_dict.update({'speed': None})
    return trips
                

        
        
# question 3 - 

def graph(trips, column_index, graphname, title):
    """
    graphs histograms of distances and speeds in bluebikes

    Parameters
    ----------
    trips : dict
    column_index : str 

    Returns
    -------
    a histogram.

    """
    # basically trying to look at the get_column function and seeing 
    # what i could apply to it
    
    values = []
    for trips_dict in trips:
        # forget the trips that should not be there
        if trips_dict[column_index] != None:
            values.append(trips_dict[column_index])
    # the "graph"
    plt.hist(values, bins = 100)
    
    

    plt.xlabel(column_index)
    plt.ylabel("Frequency")
    plt.title(title)
    plt.savefig(graphname, bbox_inches="tight")
    plt.show()
    
    return values
# 2 graphs - distances and speeds


# question 4 
def count_day(trips): 
    """
    creates a dictionary that maps day of week to count of trips with that day 
    of the week
    count_words: https://course.ccs.neu.edu/ds2000/felix_lectures/lec14_dicts_focus_part1.py
    
    Parameters
    ----------
    trips : ls of dict in TRIPS
    
    Returns
    -------
    count : dict (Day: times that trip ended up at NEU STATION)

    """
    
    count = {} # len is 0
    for trip_dict in trips:
        # end station has to == NEU Station
        end_station = trip_dict['end_station']
        if end_station == "Forsyth St at Huntington Ave":
            # if it is already in the dictionary, add to count
            if trip_dict['start_day_name'] in count: 
                count[trip_dict['start_day_name']] += 1
            # if not in dictionary, make count = 1
            else: 
                count[trip_dict['start_day_name']] = 1
        
    return count

def visualization(trips, stations):
    #i want to see how many times bike 5800 has been riden 
    count_bike_rides = {}
    for trip_dict in trips: 
        bike_id = trip_dict['bike_id']
        
        if bike_id == "5800":
            if trip_dict['bike_id'] in count_bike_rides:
                count_bike_rides[trip_dict['bike_id']] += 1
            else: 
                count_bike_rides[trip_dict['bike_id']] = 1
                # so now bike 5800 has been riden 69 times 
    

    for trip_dict in trips: 
        bike_id = trip_dict['bike_id']
        if bike_id == "5800":
                   
            coordinates_start = (stations[trip_dict['start_station']]) 
            coordinates_end = (stations[trip_dict['end_station']]) 
        
                
            # x = lat; y = long

            # plot info - i left colors as is because it looks like a nice origami 
            plt.plot([coordinates_start[1], coordinates_end[1]], [coordinates_start[0], coordinates_end[0]], linestyle='--', marker="o")

            plt.title("Bike Ride of Bike 5800")
            plt.xlabel("Latitude")
            plt.ylabel("Longitude")
            plt.savefig("singlebike.pdf", bbox_inches="tight")
            

            
    plt.show()

        

    
def main(): 
    # reading data in main
    
        
        
    trips = read_data_dict(TRIPS, type_cast_dict = {"duration": int})
    stations = read_data(STATIONS)
    calculate(trips, stations)
    
    graph(trips,'distance', "distances.pdf", "Frequency of distances of Blue Bikes")
    graph(trips, 'speed', "speeds.pdf", "Frequency of speeds of Blue Bikes")
         
    print("Number of trips ending at Forsyth St at Huntington Ave:", "\n", count_day(trips))       
    
    visualization(trips, stations)
    
    
    #point1 = [42.34414899,42.34414899]
    #point2 = [42.36466403,42.36466403]
    #print(haversine_distance(point1,point2))
    # testing the hav distance 
    
    
    
    
if __name__ == "__main__":
    main()
