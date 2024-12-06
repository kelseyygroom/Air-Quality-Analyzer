from pathlib import Path
import urllib.request
import json
import urllib.parse
from project3_failure_exceptions import api_failure, file_failure

class Location:
    def __init__(self):
        pass

    def forward_nominatim(self, location):
        '''
        Given a location description, makes a call to the Nominatim API to get
        latitidue and longitude. Returns a JSON object of the contents.
        '''

        # make url request
        url = f'https://nominatim.openstreetmap.org/search?format=json&{location}'
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)

        # convert bytes to a string
        text_bytes = response.read()
        text_str = text_bytes.decode(encoding = 'UTF-8')

        # get status code: if not 200, execute failure protocol and quit
        status = response.getcode()
        if status != 200:
            api_failure(status, url)
            quit()
    
        return text_str
 

    def coordinates(self, json_obj):
        '''
        Given the JSON object of a Nominatim API call, converts the object to a dictionary.
        Returns the latitude and longitude.
        '''
        
        try: # ensure it has desired fields/format and conver to dictionary
            json_dict = json.loads(json_obj)
            coords = float(json_dict[0]['lat']), float(json_dict[0]['lon'])
        except: # in case of failure, execute failure protocol
            fail = 'FORMAT'
            status = 200
            url = f'https://nominatim.openstreetmap.org/search'
            api_failure(status, url, fail)
            quit()
        else: 
            return coords


    def reverse_nominatim(self, lat, lon):
        '''
        Given a latitude and longitude, utilizes Nominatim API for reverse geocoding
        to find location description from coordinates.
        '''

        # make request to Nominatim API 
        request = urllib.request.Request(f'https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}')
        response = urllib.request.urlopen(request)

        # convert bytes to string
        text_bytes = response.read()
        text_str = text_bytes.decode(encoding = 'UTF-8')
        
        
        return text_str


    def file_location(self, filename):
        '''Given a path to a file, opens and reads the file, then returns the contents.'''

        # open and read file for contents
        p = Path(filename)
        file = open(p)
        contents = file.read()
        
        file.close

        return contents
        


    def reverse_location(self, json_obj):
        '''
        Given a json object from a Nominatim API call, converts it to a dictionary
        and returns the display name of the location from the API call.
        '''
    
        json_dict = json.loads(json_obj)
        location = json_dict['display_name']

        return location
        
        

class Sensor:
    def __init__(self):
        pass

    def purpleair(self):
        '''
        Makes a call to the purpleair API to obtain current air sensor information.
        Returns the response as a dictionary.
        '''

        # make request to Nominatim
        request = urllib.request.Request('https://www.purpleair.com/data.json')
        response = urllib.request.urlopen(request)

        response_bytes = response.read()
        response_str = response_bytes.decode(encoding = 'UTF-8')
        json_dict = json.loads(response_str)
        return json_dict
