import google_streetview.api as gsv
"""
Hawkhacks May 2022
Quinton Mak

A module for interacting with the google streetview api. Specifically, getting static images from a specific location.
google_streetview api: https://rrwen.github.io/google_streetview/_modules/api.html
"""


class StreetView:
    """
    key (str): the API key from google streetview to use
    dest (str): the file path in which to save the images 
    """

    def __init__(self, key, dest='images'):
        self.key = key
        self.dest = dest

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
    dest (str) is the file FOLDER to save the image to. If the folder does not exist, it will be created. The file name will be 'gsv_0' as 
        per the google streetview api.
    """

    def saveLocation(self, size, location, heading, pitch):
        params = [{
            'size': size,
            'location': location,
            'heading': heading,
            'pitch': pitch,
            'key': self.key
        }]
        results = gsv.results(params)
        results.download_links(self.dest)
        print(results.metadata)

    """
    Saves a jpg streetview image of the specified location, with the default specifications of 600x300 px, heading = 0.00, pitch = 0.00.
    For more information see the saveLocation function
    """

    def saveLocationDefault(self, location):
        self.saveLocation('600x300', location, '90.00', '0')

    """
    Returns the image file of the most recently queried location (file should be closed by user if needed to close it)
    """

    def getImage(self):
        f = open(self.dest + '\gsv_0.jpg', 'rb')
        return f
