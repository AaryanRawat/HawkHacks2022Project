from typing_extensions import Self
from unicodedata import name
import numpy as np
import pandas as pd
from pandasql import sqldf
from streetview import StreetView
from math import cos, asin, sqrt

pysqldf = lambda q: sqldf(q, globals())
lsqldf = lambda q: sqldf(q, locals())


class Playlist:
    """
    path (str): the file path of the playlist data
    """

    def __init__(self, path=None, name=None):
        if (path): self.locations = self.listOfLocation(path)
        else:
            # set it manually, I guess
            print()
        self.name = name

    """
    Returns a (listof dict) from an excel file. 
    The file must have a column named 'location' and can have other optional columns.
    Each dict corresponds to a row in the spreadsheet. 
    Each field corresponds to a column in the spreadsheet.
    """

    def listOfLocation(self, path):
        try:
            df = pd.read_excel(path)
        except PermissionError:
            print("Make sure the source excel file is not open!")
            return
        if ('location' not in df):
            print("Excel file must have the required columns!")
            return
        df = sqldf("SELECT * FROM df", locals())
        cols = df.columns
        list = df.values.tolist()
        returnlist = [{col: val
                       for col, val in zip(cols, item)} for item in list]
        return returnlist

    # Haversine formula for finding distance on a sphere
    def distance(self, lat1, lon1, lat2, lon2):
        p = 0.017453292519943295  # Pi / 180
        a = 0.5 - cos(
            (lat2 - lat1) * p) / 2 + cos(lat1 * p) * cos(lat2 * p) * (1 - cos(
                (lon2 - lon1) * p)) / 2
        return 12742 * asin(sqrt(a))  # Diameter of earth = 12742 km
