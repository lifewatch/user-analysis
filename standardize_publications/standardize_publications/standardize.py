# import statements
import pandas as pd
import numpy as np
import os

# import pycountry
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

import logging
from logging import NullHandler

log = logging.getLogger(__name__)
log.addHandler(NullHandler())


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
        Check for extact matches between 'Institute' (from Affiliation_Standardized) and 'Affiliation' (from IMIS) or 'wos_affil' (from adding the wos export);
        and adds 'Institute Standardized' to stand_affil in case of exact match.
        :param stand_file: standardized data file
        :type stand_file: str
        """

        self.stand_data = load_filedata(stand_file)

        # Find exact match & add standardized affiliation: - note: not most efficient way to do this, but it works for now...
        self.data["stand_affil"] = ""
        col_index = self.data.columns.get_loc("stand_affil")

        for index, row in self.data.iterrows():
            print(index, row["Affiliation"])
            no_exact_match = True
            for index2, row2 in self.stand_data.iterrows():

                if (
                    "Affiliation" in self.data.columns
                    and isinstance(row["Affiliation"], str)
                    and no_exact_match == True
                ):
                    # check and add first found match:
                    if row["Affiliation"] == row2["Institute"]:
                        self.data.iloc[index, col_index] = [
                            row2["Institute standardized"]
                        ]
                        no_exact_match = False

                elif (
                    "wos_affil" in self.data.columns
                    and isinstance(row["wos_affil"], str)
                    and no_exact_match == True
                ):
                    # check & add first found match:
                    if row["wos_affil"] == row2["Institute"]:
                        self.data.iloc[index, col_index] = [
                            row2["Institute standardized"]
                        ]
                        no_exact_match = False

        return self

    def similarityMatch(self, stand_file: str) -> pd.DataFrame:
        """
        Check similarity between 'Institute standardized' and 'raw' affiliation names in the data (columns 'Affiliation' or 'wos_affil').
        In case of a similarity higher than 80%, the standardized affiliation name is added in the 'stand_affil' column.

        :param stand_file: standardized data file
        :type stand_file: str
        """

        self.stand_data = load_filedata(stand_file)

        # Find similarity match & add standardized affiliation: - note: not most efficient way to do this, but it works for now...
        standaffil_index = self.data.columns.get_loc("stand_affil")
        self.data["similarity_method"] = ""
        standaffil_method_index = self.data.columns.get_loc("similarity_method")

        for index, row in self.data.iterrows():
            if len(row["stand_affil"]) == 0:

                if "Affiliation" in self.data.columns and isinstance(
                    row["Affiliation"], str
                ):
                    print(row["Affiliation"])
                    best_Affil_match = best_standmatch(
                        self.stand_data, row["Affiliation"]
                    )
                    if best_Affil_match:
                        print(
                            "found best_affil_match for 'Affiliation': ",
                            best_Affil_match,
                        )
                        self.data.iloc[index, standaffil_index] = best_Affil_match
                        self.data.iloc[index, standaffil_method_index] = "x"

                elif "wos_affil" in self.data.columns and isinstance(
                    row["wos_affil"], str
                ):
                    print(row["wos_affil"])
                    best_wosAffil_match = best_standmatch(
                        self.stand_data, row["wos_affil"]
                    )
                    if best_wosAffil_match:
                        print(
                            "found best_affil_match for 'wos_affil': ",
                            best_wosAffil_match,
                        )
                        self.data.iloc[index, standaffil_index] = best_wosAffil_match
                        self.data.iloc[index, standaffil_method_index] = "x"

        return self

    def add_affilinfo(self, affil_info: str):

        # load affiliation info:
        self.affilinfo = load_filedata(affil_info)

        # for each standard affiliation, add affilation information:
        self.data["stand_country"] = ""
        stand_country_index = self.data.columns.get_loc("stand_country")
        self.data["stand_flemish"] = ""
        stand_flemish_index = self.data.columns.get_loc("stand_flemish")
        self.data["stand_GROUP"] = ""
        stand_GROUP_index = self.data.columns.get_loc("stand_GROUP")
        self.data["stand_QH"] = ""
        QH_index = self.data.columns.get_loc("stand_QH")

        for (
            index,
            row,
        ) in (
            self.data.iterrows()
        ):  # note: again, very unefficient, but it works for now...

            for index2, row2 in self.affilinfo.iterrows():

                if row["stand_affil"] == row2["Institute_stand_check"]:
                    self.data.iloc[index, stand_country_index] = row2["Country_stand"]
                    self.data.iloc[index, stand_flemish_index] = row2["Flemish"]
                    self.data.iloc[index, stand_GROUP_index] = row2["GROUP"]
                    self.data.iloc[index, QH_index] = row2["QH"]

        return self

    """def add_standcountry(self):

        # should be: if country (from standardizing 'Affiliation' column) or wos_country are present --> country_stand col added with standardized country names
        # for now only adding with wos_country as standardizing of affiliation info not working yet
        'stand_country'
        print("Adding standardized country information, this could take a while...")
        for index, row in self.data.iterrows():
            
            if isinstance(row['stand_country'], str):
                country = pycountry.countries.search_fuzzy(str(row["wos_country"]))
                #alpha2code = country[0].

            elif isinstance(row['wos_country'], str):
                pass
            
            #if row["wos_country"] == 'South Korea' or row["wos_country"] == 'Peoples R China' or row["wos_country"] == 'North Ireland' or row["wos_country"] == 'Bosnia & Herceg': #seems to break on these
"""
