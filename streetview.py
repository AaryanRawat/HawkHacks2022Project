import google_streetview.api as gsv
import googlemaps
"""
Hawkhacks May 2022

A module for interacting with the google streetview api. Specifically, getting static images from a specific location.
google_streetview api: https://rrwen.github.io/google_streetview/_modules/api.html
Nominatim api: https://geopy.readthedocs.io/en/stable/#nominatim
Note: Because of the way google_streetview API works, you can only access the most recent query at a time. 
"""


class StreetView:
    """
    key (str): the API key from google streetview to use
    dest (str): the file path in which to save the images 
    """

    def __init__(self, key, dest='images'):
        self.__key = key
        self.dest = dest
        self.params = {}
        self.metadata = None

    """
    Saves a jpg streetview image of the specified location.

    size (str) is the dimensions of the saved image file (jpg). Formatted as 'size': '600x300', max 640x640 pixels.
    location (str) can be either a text string (such as Chagrin Falls, OH) or a lat/lng value (40.457375,-80.009353), 
        and should be URL-encoded, so addresses such as "City Hall, New York, NY" should be converted to "City+Hall,New+York,NY",
        before the request is signed. The Street View Static API will snap to the panorama photographed closest to this location.
        When an address text string is provided, the API may use a different camera location to better display the specified location. 
        When a lat/lng is provided, the API searches a 50 meter radius for a photograph closest to this location. 
        Because Street View imagery is periodically refreshed, and photographs may be taken from slightly different positions each time,
        it's possible that your location may snap to a different panorama when imagery is updated.
    heading (str) indicates the compass heading of the camera. Formatted as '151.78'. Values range from 0 to 360.
    pitch (str) specifies the up or down angle of the camera. Formatted as 'pitch': '-0.76'. Values range from -90 to 90.
            'key': 'your_dev_key'
        }]
    From Google Streeetview Static API: 
        location can be either a text string (such as Chagrin Falls, OH) or a lat/lng value (40.457375,-80.009353), 
        and should be URL-encoded, so addresses such as "City Hall, New York, NY" should be converted to "City+Hall,New+York,NY",
        before the request is signed. The Street View Static API will snap to the panorama photographed closest to this location.
        When an address text string is provided, the API may use a different camera location to better display the specified location. 
        When a lat/lng is provided, the API searches a 50 meter radius for a photograph closest to this location. 
        Because Street View imagery is periodically refreshed, and photographs may be taken from slightly different positions each time,
        it's possible that your location may snap to a different panorama when imagery is updated.
        Note: I don't think URL encoding is needed, a normal string should work fine for this API
    dest (str) is the file FOLDER to save the image to. If the folder does not exist, it will be created. The file name will be 'gsv_0' as 
        per the google streetview api.
    """

    def saveLocation(self, size, location, heading, pitch):
        self.params = {
            'size': size,
            'location': location,
            'heading': heading,
            'pitch': pitch,
            'key': self.__key
        }
        params = [self.params]
        results = gsv.results(params)
        results.download_links(self.dest)
        self.metadata = results.metadata

    """
    Saves a jpg streetview image of the specified location, with the default specifications of 600x300 px, heading = 0.00, pitch = 0.00.
    For more information see the saveLocation function
    """

    def saveLocationDefault(self, location):
        self.saveLocation('600x300', location, '90.00', '0')

    """
    Returns the image file of the most recently queried location
    """

    def getImage(self):
        with open(self.dest + '\gsv_0.jpg',
                  'rb') as f:  #earlier code left a file handle open
            img = f.read()
        return img
        # f = open(self.dest + '\gsv_0.jpg', 'rb')
        # return f

    """
    Returns the  metadata of the most recently queried object

    Example return format:
    {'size': '600x300', 'location': {'lat': 43.0791675, 'lng': -79.0788306}, 'heading': '90.00', 
    'pitch': '0', 'key': YOUR_KEY, 'copyright': '© Alec Coder', 
    'date': '2017-07', 'pano_id': 'CAoSLEFGMVFpcE5Ob01EWVNkdzA3YkoxRUtTX1dhS2Fka294Y3VUekh2N1MtbGhE', 
    'status': 'OK', '_file': 'gsv_0.jpg'}
    """

    def getMetadata(self):
        metadict = self.metadata[0]
        return self.params | metadict

    """
    Returns the coordinates in latitude and longitude of the most recently queried location, as a dictionary
    Return format: {'lat':___, 'lng':___}
    """

    def getCurrentCoordinates(self):
        coords = self.getMetadata()['location']
        return coords

    """
    Returns the formatted address of the most recently queried location as a str
    """

    def getCurrentAddress(self):
        coords = self.getMetadata()['location']
        return self.getAddress(coords)

    """
    Gets the latitude and longitude of the given location, as a dictionary
    location (str) represents the address of the place
    Return format: {'lat':___, 'lng':___} 
    """

    def getCoordinates(self, location):
        gmaps = googlemaps.Client(key=self.__key)
        geocode_result = gmaps.geocode(location)
        return geocode_result[0]['geometry']['location']

    """
    Gets a formatted address of the given location
    location is either a 
        (str)
        (lat, long) tuple
        {'lat':___, 'lng':___} formatted dict
    which represents the address of the place
    """

    def getAddress(self, location):
        gmaps = googlemaps.Client(key=self.__key)
        if (type(location) == str):
            geocode_result = gmaps.geocode(location)
        elif (type(location) == tuple):
            geocode_result = gmaps.reverse_geocode(location)
        elif (type(location) == dict):
            geocode_result = gmaps.reverse_geocode(tuple(location.values()))
        return geocode_result[0]['formatted_address']

    """
    Returns a dictionary containing all of the raw geocode data of the given location
    location is either a 
        (str)
        (lat, long) tuple
        {'lat':___, 'lng':___} formatted dict
    which represents the address of the place
    """

    def getAllGeodata(self, location):
        gmaps = googlemaps.Client(key=self.__key)
        if (type(location) == str):
            geocode_result = gmaps.geocode(location)
        elif (type(location) == tuple):
            geocode_result = gmaps.reverse_geocode(location)
        elif (type(location) == dict):
            geocode_result = gmaps.reverse_geocode(tuple(location.values()))
        return geocode_result[0]