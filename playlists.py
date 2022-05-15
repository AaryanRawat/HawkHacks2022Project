from typing_extensions import Self
import numpy as np
import pandas as pd
from pandasql import sqldf
from streetview import StreetView

pysqldf = lambda q: sqldf(q, globals())
lsqldf = lambda q: sqldf(q, locals())
"""
    Returns a (listof dict) from an excel file. 
    The file must have a column named 'location' and can have other optional columns.
    Each dict corresponds to a row in the spreadsheet. 
    Each field corresponds to a column in the spreadsheet.
"""


class Playlist:
    """
    path (str): the file path of the playlist data
    """

    def __init__(self, path=None):
        if (path): self.locations = self.listOfLocation(path)
        else:
            # set it manually, I guess
            print()

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