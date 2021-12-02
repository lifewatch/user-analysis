import pandas as pd
import os
from .functions import load_folderdata, update_datafile


class WOS:

    def __init__(self, data, wos_export: str) -> pd.DataFrame:

        self.data = data
        self.export_data = load_folderdata(wos_export, 'wos_export')

    def add_WOSaffil(self) -> pd.DataFrame:
        """Add affiliation information of the first author, exported from Web of Science"""

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
        return self

    def add_WOScountry(self) -> pd.DataFrame:
        """Add the country of the affiliation of the first author, exported from Web of Science"""

        if 'wos_country' not in self.data.columns:
            for index, row in self.export_data.iterrows():
                # get country name from string & clean up
                country_firstauth = str(row['RP']).split(
                    ', ')[-1]
                country_firstauth = country_firstauth.rstrip(
                    country_firstauth[-1])
                if 'USA' in country_firstauth:
                    country_firstauth = 'USA'
                self.data.loc[self.data['WoScode'] == row['UT'],
                              "wos_country"] = country_firstauth
        return self

    def add_WOSkeywords(self) -> pd.DataFrame:
        """Add the country of the affiliation of the first author, exported from Web of Science"""

        if 'wos_keywords' not in self.data.columns:
            for index, row in self.export_data.iterrows():
                keywords = row['DE']
                self.data.loc[self.data['WoScode'] == row['UT'],
                              "wos_keywords"] = keywords
        return self

    def add_WOSpluskeywords(self) -> pd.DataFrame:
        """Add the country of the affiliation of the first author, exported from Web of Science"""

        if 'wos_plus_keywords' not in self.data.columns:
            for index, row in self.export_data.iterrows():
                pluskeywords = row['ID']
                self.data.loc[self.data['WoScode'] == row['UT'],
                              "wos_plus_keywords"] = pluskeywords
        return self

    def add_WOScategories(self) -> pd.DataFrame:
        """Add the country of the affiliation of the first author, exported from Web of Science"""

        if 'wos_categories' not in self.data.columns:
            for index, row in self.export_data.iterrows():
                categories = row['WC']
                self.data.loc[self.data['WoScode'] == row['UT'],
                              "wos_categories"] = categories
        return self

    def add_WOSresearcharea(self) -> pd.DataFrame:
        """Add the country of the affiliation of the first author, exported from Web of Science"""

        if 'wos_researcharea' not in self.data.columns:
            for index, row in self.export_data.iterrows():
                researcArea = row['SC']
                self.data.loc[self.data['WoScode'] == row['UT'],
                              "wos_researcharea"] = researcArea
        return self

    def add_WOScitations(self) -> pd.DataFrame:
        """Add the country of the affiliation of the first author, exported from Web of Science"""

        if 'wos_citations' not in self.data.columns:
            for index, row in self.export_data.iterrows():
                citations = row['NR']
                citations_ref = row['CR']
                self.data.loc[self.data['WoScode'] == row['UT'],
                              "wos_citations"] = citations
                self.data.loc[self.data['WoScode'] == row['UT'],
                              "wos_citation_refs"] = citations_ref
        return self

    def add_WOSusage(self) -> pd.DataFrame:
        """Add the country of the affiliation of the first author, exported from Web of Science"""

        if 'wos_usage' not in self.data.columns:
            for index, row in self.export_data.iterrows():
                citations = row['U2']
                self.data.loc[self.data['WoScode'] == row['UT'],
                              "wos_usage"] = citations
        return self
