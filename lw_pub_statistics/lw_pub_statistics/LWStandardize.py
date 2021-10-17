# import statements
import pandas as pd
import numpy as np
import os
import shutil
from pandas._testing import assert_index_equal
from pandas.api.types import is_string_dtype

from .functions import load_folderdata, load_filedata, best_standmatch, update_datafile


class Standardizator:

    def __init__(self, pubfolder: str) -> pd.DataFrame:
        """
        constructor

        :param file: name of folder with publication info
        :type file: str
        :returns: dataframe object of publication files in folder
        :rtype: pd.DataFrame
        """

        # load standardized data if present, otherwise load non stand data:
        if os.path.isfile(os.path.join(os.pardir, 'standardized_data', 'stand_data.csv')):
            self.data = load_filedata(os.path.join(
                os.pardir, 'standardized_data', 'stand_data.csv'))
        else:
            self.data = load_folderdata(pubfolder, 'publication_data')

    def add_WOSaffil(self, wos_export: str) -> pd.DataFrame:
        """
        Add affiliation information of the first author, exported from Web of Science
        :param stand_file: folder with wos export files
        :type stand_file: str
        """

        self.export_data = load_folderdata(wos_export, 'wos_export')

        if 'wos_affil' not in self.data.columns:
            for index1, row in self.export_data.iterrows():
                # note: type of nan values in export_data['RP'] is float, which is non iterable
                if type(row['RP']) == str:
                    # 1. wos affiliation of first author | 'RP' = first author name & affiliation info ; 'RP_2' = first author affiliation info
                    affil_firstauth = str(row['RP']).split(
                        '(corresponding author), ')[-1]
                    # 2. add wos_affil to data based on wos code | 'UT' = wos code
                    self.data.loc[self.data['WoScode'] == row['UT'],
                                  "wos_affil"] = affil_firstauth

            update_datafile(self.data)
            print("WoS affiliations added to %s" % os.path.join(
                os.pardir, 'standardized_data', 'stand_data.csv'))

        return self

    def add_WOScountry(self, wos_export: str) -> pd.DataFrame:
        """
        Add the country of the affiliation of the first author, exported from Web of Science
        :param stand_file: folder with wos export files
        :type stand_file: str
        """

        # Read data
        self.export_data = load_folderdata(wos_export, 'wos_export')

        if 'wos_country' not in self.data.columns:
            # 1. wos affiliation of first author | 'RP' = first author name & affiliation info
            for index, row in self.export_data.iterrows():
                # get country name from string & clean up
                country_firstauth = str(row['RP']).split(
                    ', ')[-1]
                country_firstauth = country_firstauth.rstrip(
                    country_firstauth[-1])
                if 'USA' in country_firstauth:
                    country_firstauth = 'USA'

                # 2. add wos_affil to data based on wos code | 'UT' = wos code
                self.data.loc[self.data['WoScode'] == row['UT'],
                              "wos_country"] = country_firstauth

            # update datafile
            update_datafile(self.data)
            print("Country information added to %s" % os.path.join(
                os.pardir, 'standardized_data', 'stand_data.csv'))
        return self

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
        if 'stand_method' not in self.data.columns or 'exact match' not in self.data['stand_method']:
            for index, row in self.stand_data.iterrows():
                self.data.loc[self.data['Affiliation'] == row['Institute'],
                              "stand_affil"] = row['Institute standardized']
                self.data.loc[self.data['Affiliation'] == row['Institute'],
                              "stand_method"] = 'exact match'

            update_datafile(self.data)
            print("Added exact matches between 'Affiliation' column and 'Institute' column from standardized list to %s" %
                  os.path.join(os.pardir, 'standardized_data', 'stand_data.csv'))

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

        col_text = 'similarity match %s' % col_stand
        if 'stand_method' not in self.data.columns or col_text not in self.data['stand_method']:
            print(col_text)
            """# select a subset of data that isn't standardized yet
            if 'stand_affil' in self.data.columns:
                self.nonstand_data = self.data.loc[
                    self.data['stand_affil'] == 'nan']
            else:
                self.nonstand_data = self.data"""

            # standardize data
            for index1, row1 in self.data.iterrows():
                stand_affil = row1['stand_affil']

                # non stand data:
                if type(stand_affil) == float:
                    affiliation = str(row1[col_stand])

                    best_match = best_standmatch(
                        self.stand_data, affiliation)
                    print(best_match)
                    if best_match is not None:
                        stand_affil = best_match

                self.data.at[index1, 'stand_affil'] = stand_affil
                self.data.at[index1, 'stand_method'] = col_text

            update_datafile(self.data)
            print("0.80 similar matches between %s column and 'Institute' column from standardized list were added to %s" % (
                  col_stand, os.path.join(os.pardir, 'standardized_data', 'stand_data.csv')))

        return self
