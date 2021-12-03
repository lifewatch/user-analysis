# import statements
import pandas as pd
import numpy as np
import os
from pathlib import Path
from pandas._testing import assert_index_equal
from pandas.api.types import is_string_dtype

from .functions import (
    # load_folderdata,
    load_filedata,
    best_standmatch,
    # update_datafile,
    write_filedata,
)
from .wos import *


class Standardizator:
    def __init__(self, pubfile: str, reffile: str) -> pd.DataFrame:
        """
        constructor

        :param pubfile: name of file with publication info
        :type file: str
        :returns: dataframe object of publication files in folder
        :rtype: pd.DataFrame
        """

        self.pubfile = pubfile
        self.reffile = reffile
        # non-standardized data:
        self.data = load_filedata(os.path.abspath(self.pubfile))
        # standardized reference affiliations:
        self.refdata = load_filedata(os.path.abspath(self.reffile))

    def add_wosinfo(self, wos_export: str) -> pd.DataFrame:
        """Add information from wos_export"""

        wos_data = load_folderdata(wos_export)
        self.data = add_WOSaffil(self.data, wos_data)
        self.data = add_WOScountry(self.data, wos_data)
        self.data = add_WOSkeywords(self.data, wos_data)
        self.data = add_WOSpluskeywords(self.data, wos_data)
        self.data = add_WOScategories(self.data, wos_data)
        self.data = add_WOSresearcharea(self.data, wos_data)
        # self.data = add_WOScitations(self.data, wos_data)
        # self.data = add_WOSusage(self.data, wos_data)
        return self

    def to_file(self, standdatafile):
        # note: file gets overwritten if exists already
        write_filedata(self.data, standdatafile)

    def exactMatch(self, stand_file: str) -> pd.DataFrame:
        """
        Check for extact matches between 'Affiliation' (from IMIS) and 'Institute' (from Affiliation_Standardized);
        and adds 'Institute Standardized' to stand_affil in case of exact match.
        :param stand_file: standardized data file
        :type stand_file: str
        """

        # Load standardized affiliation names:
        self.stand_data = load_filedata(stand_file)

        # Find exact match & add standardized affiliation:
        if (
            "stand_method" not in self.data.columns
            or "exact match" not in self.data["stand_method"]
        ):
            for index, row in self.stand_data.iterrows():
                self.data.loc[
                    self.data["Affiliation"] == row["Institute"], "stand_affil"
                ] = row["Institute standardized"]
                self.data.loc[
                    self.data["Affiliation"] == row["Institute"], "stand_method"
                ] = "exact match"

            # update_datafile(self.data)
            print(
                "Added exact matches between 'Affiliation' column and 'Institute' column from standardized list to %s"
                % os.path.join(os.pardir, "standardized_data", "stand_data.csv")
            )

        return self

    def similarityMatch(self, stand_file: str, col_stand: str) -> pd.DataFrame:
        """
        Check similarity between 'Institute standardized' and 'raw' affiliation names in the data (columns 'Affiliation' or 'wos_affil').
        In case of a similarity higher than 80%, the standardized affiliation name is added in the 'stand_affil' column.

        :param stand_file: standardized data file
        :type stand_file: str
        """

        # Load standardized affiliation names:
        self.stand_data = load_filedata(stand_file)

        col_text = "similarity match %s" % col_stand
        if (
            "stand_method" not in self.data.columns
            or col_text not in self.data["stand_method"]
        ):
            print(col_text)
            """# select a subset of data that isn't standardized yet
            if 'stand_affil' in self.data.columns:
                self.nonstand_data = self.data.loc[
                    self.data['stand_affil'] == 'nan']
            else:
                self.nonstand_data = self.data"""

            # standardize data
            for index1, row1 in self.data.iterrows():
                stand_affil = row1["stand_affil"]

                # non stand data:
                if type(stand_affil) == float:
                    affiliation = str(row1[col_stand])

                    best_match = best_standmatch(self.stand_data, affiliation)
                    print(best_match)
                    if best_match is not None:
                        stand_affil = best_match

                self.data.at[index1, "stand_affil"] = stand_affil
                self.data.at[index1, "stand_method"] = col_text

            # update_datafile(self.data)
            print(
                "0.80 similar matches between %s column and 'Institute' column from standardized list were added to %s"
                % (
                    col_stand,
                    os.path.join(os.pardir, "standardized_data", "stand_data.csv"),
                )
            )

        return self
