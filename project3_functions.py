import math
from pathlib import Path
from project3_classes import Location, Sensor
import json
from operator import itemgetter
import urllib.request
import urllib.parse


def distance(lat1, lon1, lat2, lon2):
    '''
    Calculates the distance between two locations, given both location's latitudes
    and longitudes. Returns an integer that is the distance between locations.
    '''

    if lat2 == None:
        return None
    elif lon2 == None:
        return None
    
    dlat = math.radians(lat1 - lat2)
    dlon = math.radians(lon1 - lon2)
    alat = math.radians((lat1 + lat2)/2)
    R = 3958.8
    x = dlon * (math.cos(alat))
    d = math.sqrt((x ** 2) + (dlat ** 2)) * R

    return d
        
    

def lat_lon(center_input):
    '''
    Given the center input, takes action based on the format - making a call to
    Nominatim API or opening a file, and obtains the center coordinates.
    '''

    if 'CENTER NOMINATIM' in center_input:
        center = center_input.split('CENTER NOMINATIM ')[1].lower()
        c = urllib.parse.urlencode([('q', center)])
        x = Location()
        json_contents = x.forward_nominatim(c)

        return x.coordinates(json_contents)
    
    elif 'CENTER FILE ' in center_input:
        # isolate the path
        p = Path(center_input.split('CENTER FILE ')[1])
        
        # get the latitude and longitude from file
        file = open(p)
        contents = file.read()

        # assign x as Location object
        x = Location()

        # get the coordinates from the file
        c = x.coordinates(contents)
            
        file.close

        return c


def sensors(source):
    '''
    Given an input that indicates where to obtain air quality info, determines
    the source and either makes a call to the Purplair API or opens a file.
    Returns the air quality info as a dictionary.
    '''

    # calls purpleair API from the Sensor class if the source is AQI PURPLEAIR
    if 'AQI PURPLEAIR' in source:
        y = Sensor()
        aq_info = y.purpleair()
        
        return aq_info

    # gets aqi info froma file path
    elif 'AQI FILE' in source:
        x = Sensor()
    
        path = source.split('AQI FILE ')[1]
        p = Path(path)

        file = open(p, 'r', encoding='utf-8')

        try:
            aq_info = file.read()
            json_dict = json.loads(aq_info)
        except:
            file_failure(path, 'FORMAT')
        
        return json_dict



def aqi_lst(sensors_lst):
    '''
    Given a two_dimensional list of sensors with with air quality expressed in terms of pm,
    calculates the AQI value and returns a list where pm is appended with the AQI value.
    '''

    appended = []
    
    for sensor in sensors_lst:
        pm = sensor[1]

        # excludes any null values
        if pm == None:
            pass

        # perform conversions from pm to aqi 
        elif 0.0 <= pm < 12.1:
            l_pm = 0.0
            u_pm = 12.0
            l_aqi = 0
            u_aqi = 50
            
            ratio = (pm - l_pm)/(u_pm - l_pm)
            difference = (u_aqi - l_aqi) * (ratio)
            aqi = round(l_aqi + difference)

            sensor[1] = aqi
            appended.append(sensor)

        elif 12.1 <= pm < 35.5:
            l_pm = 12.1
            u_pm = 35.4
            l_aqi = 51
            u_aqi = 100
            
            ratio = (pm - l_pm)/ (u_pm - l_pm)
            difference = (u_aqi - l_aqi) * (ratio)
            aqi = round(l_aqi + difference)

            sensor[1] = aqi
            appended.append(sensor)

        elif 35.5 <= pm < 55.5:
            l_pm = 35.5
            u_pm = 55.4
            l_aqi = 101
            u_aqi = 150
            
            ratio = (pm - l_pm)/ (u_pm - l_pm)
            difference = (u_aqi - l_aqi) * (ratio)
            aqi = round(l_aqi + difference)

            sensor[1] = aqi
            appended.append(sensor)

        elif 55.5 <= pm < 150.5:
            l_pm = 55.5
            u_pm = 150.4
            l_aqi = 151
            u_aqi = 200
            
            ratio = (pm - l_pm)/ (u_pm - l_pm)
            difference = (u_aqi - l_aqi) * (ratio)
            aqi = round(l_aqi + difference)

            sensor[1] = aqi
            appended.append(sensor)

        elif 150.5 <= pm < 250.5:
            l_pm = 150.5
            u_pm = 250.4
            l_aqi = 201
            u_aqi = 300
            
            ratio = (pm - l_pm)/ (u_pm - l_pm)
            difference = (u_aqi - l_aqi) * (ratio)
            aqi = round(l_aqi + difference)

            sensor[1] = aqi
            appended.append(sensor)

        elif 250.5 <= pm < 350.5:
            l_pm = 250.5
            u_pm = 350.4
            l_aqi = 301
            u_aqi = 400
            
            ratio = (pm - l_pm)/ (u_pm - l_pm)
            difference = (u_aqi - l_aqi) * (ratio)
            aqi = round(l_aqi + difference)

            sensor[1] = aqi
            appended.append(sensor)

        elif 350.5 <= pm < 500.5:
            l_pm = 350.5
            u_pm = 500.4
            l_aqi = 401
            u_aqi = 500
            
            ratio = (pm - l_pm)/ (u_pm - l_pm)
            difference = (u_aqi - l_aqi) * (ratio)
            aqi = round(l_aqi + difference)

            sensor[1] = aqi
            appended.append(sensor)

        elif pm >= 500.5:
            aqi = 501

            sensor[1] = aqi
            appended.append(sensor)

    # return list of sensor data where pm has been replaced with aqi
    return appended
            


def valid_sensors(threshold, sensors_lst, max_num):
    '''Iterates through a two-dimensional list of sensor data. Constructs a new
    list with only valid sensor locations where the sensor is located outdoors,
    the age is < 3600 seconds, and the aqi is within the threshold. 
    '''

    all_sensors = []

    for sensor_data in sensors_lst:
        if (sensor_data[1] == None) or (sensor_data[25] == None) or (sensor_data[4] == None):
            pass # exclude null values
        elif sensor_data[25] == 1:
            pass # exclude indoor sensors
        elif sensor_data[4] > 3600:
            pass # exclude sensors where age > 1hr
        else:
            all_sensors.append(sensor_data) # if it passes all prior tests, append

    unsorted_aqis = aqi_lst(all_sensors)

    # ensures that all aqi values are higher than threshold
    threshold_aqis = []
    for sensor in unsorted_aqis:
        if sensor[1] > threshold:
            threshold_aqis.append(sensor)

    # sorts by aqi column, highest to lowest
    sorted_aqis = sorted(threshold_aqis, key=itemgetter(1), reverse=True)

    final_aqis = sorted_aqis[0:max_num]
            
    return final_aqis    


def sensors_in_range(center, rnge, sensor_lst: [list]) -> [list]:
    '''
    Given a center latitude and longitude, a range, and a two-dimensional list, makes a call
    to the distance function and returns another two-dimensional list of sensor locations
    within the given range.
    '''
    
    clat = float(center[0])
    clon = float(center[1])

    in_range = []

    # call distance function to see if location is within range
    for sensor_data in sensor_lst:
        if distance(clat, clon, sensor_data[27], sensor_data[28]) == None:
            pass # exclude null values
        elif distance(clat, clon, sensor_data[27], sensor_data[28]) < rnge:
            in_range.append(sensor_data)

    return in_range


def reverse_source(reverse_input):
    '''Returns the source to be used for reverse geocoding.'''
    
    if 'REVERSE NOMINATIM' in reverse_input:
        return 'API'
    elif 'REVERSE FILES' in reverse_input:
        r = reverse_input.split('REVERSE FILES ')[1]
        return r.split()


def print_all_data(center_coords, sensors_lst, reverse_source):
    '''
    Given center coordinates, a two-dimensional list of sensor data, and the
    source to be used for reverse geocoding, prints all sensor data in the
    desired format.
    '''

    # prints center data in the desired format: negative coordinates are S/W
    if center_coords[0] > 0:
        c_lat = f'{center_coords[0]}/N'
    else:
        abs_c_lat = abs(center_coords[0])
        c_lat = f'{abs_c_lat}/S'

    if center_coords[1] > 0:
        c_lon = f'{center_coords[1]}/E'
    else:
        abs_c_lon = abs(center_coords[1])
        c_lon = f'{abs_c_lon}/W'


    print(f'CENTER {c_lat} {c_lon}')
    
    counter = 0

    # prints sensor data in desired format
    for sensor in sensors_lst:
        aqi = sensor[1]
        lat = sensor[27]
        lon = sensor[28]
        print(f'AQI {aqi}')
        if lat > 0:
            print(f'{lat}/N', end=' ')
        else:
            abs_lat = abs(lat)
            print(f'{abs_lat}/S',end=' ')

        if lon > 0:
            print(f'{lon}/E')
        else:
            abs_lon = abs(lon)
            print(f'{abs_lon}/W')
        
        if reverse_source == 'API':
            x = Location()
            json_object = x.reverse_nominatim(lat, lon)
            location = x.reverse_location(json_object)
            print(location)
        else:
            x = Location()
            json_object = x.file_location(reverse_source[counter])
            location = x.reverse_location(json_object)
            counter += 1
            print(location)
    
