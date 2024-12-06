from pathlib import Path
import urllib.request
import json
import urllib.parse
import math
from operator import itemgetter
import project3_functions

        

def run():

    # get input for center location and obtain coordinates of the center
    center = input()
    coordinates = project3_functions.lat_lon(center)


    # take input for the range to search for sensors
    rnge = input()
    miles = int(rnge.split('RANGE ')[1])


    # get the threshold value for AQIs
    thresh = input()
    threshold = int(thresh.split('THRESHOLD ')[1])


    # get a max number of sensor locations to return 
    max_inp = input()
    max_num = int(max_inp.split('MAX ')[1])

    # get a source for the sensor data - file vs. API
    source = input()
    all_sensors = project3_functions.sensors(source)
    sensor_data = all_sensors['data']


    # get a source for reverse geocoding
    reverse = input()
    r_source = project3_functions.reverse_source(reverse)


    # filter through and return sensor data that meets all parameters
    sensors_in_distance = project3_functions.sensors_in_range(coordinates, miles, sensor_data)
    all_valid_sensors = project3_functions.valid_sensors(threshold, sensors_in_distance, max_num)

    # print all the data: center, sensors, etc...
    project3_functions.print_all_data(coordinates, all_valid_sensors, r_source)
    
    


if __name__ == '__main__':

    # start run function
    run()

