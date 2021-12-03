import pandas as pd
import os
from .functions import load_folderdata, update_datafile


def add_WOSaffil(data: pd.DataFrame, wos_export: pd.DataFrame) -> pd.DataFrame:
    """Add affiliation information of the first author, exported from Web of Science"""

    if "wos_affil" not in data.columns:
        for index1, row in wos_export.iterrows():
            # note: type of nan values in export_data['RP'] is float, which is non iterable
            if type(row["RP"]) == str:
                # 1. wos affiliation of first author | 'RP' = first author name & affiliation info ; 'RP_2' = first author affiliation info
                affil_firstauth = str(row["RP"]).split("(corresponding author), ")[-1]
                # 2. add wos_affil to data based on wos code | 'UT' = wos code
                data.loc[data["WoScode"] == row["UT"], "wos_affil"] = affil_firstauth
    return data


def add_WOScountry(data: pd.DataFrame, wos_export: pd.DataFrame) -> pd.DataFrame:
    """Add the country of the affiliation of the first author, exported from Web of Science"""

    if "wos_country" not in data.columns:
        for index, row in wos_export.iterrows():
            # get country name from string & clean up
            country_firstauth = str(row["RP"]).split(", ")[-1]
            country_firstauth = country_firstauth.rstrip(country_firstauth[-1])
            if "USA" in country_firstauth:
                country_firstauth = "USA"
            data.loc[data["WoScode"] == row["UT"], "wos_country"] = country_firstauth
    return data


def add_WOSkeywords(data: pd.DataFrame, wos_export: pd.DataFrame) -> pd.DataFrame:
    """Add the country of the affiliation of the first author, exported from Web of Science"""

    if "wos_keywords" not in data.columns:
        for index, row in wos_export.iterrows():
            keywords = row["DE"]
            data.loc[data["WoScode"] == row["UT"], "wos_keywords"] = keywords
    return data


def add_WOSpluskeywords(data: pd.DataFrame, wos_export: pd.DataFrame) -> pd.DataFrame:
    """Add the country of the affiliation of the first author, exported from Web of Science"""

    if "wos_plus_keywords" not in data.columns:
        for index, row in wos_export.iterrows():
            pluskeywords = row["ID"]
            data.loc[data["WoScode"] == row["UT"], "wos_plus_keywords"] = pluskeywords
    return data


def add_WOScategories(data: pd.DataFrame, wos_export: pd.DataFrame) -> pd.DataFrame:
    """Add the country of the affiliation of the first author, exported from Web of Science"""

    if "wos_categories" not in data.columns:
        for index, row in wos_export.iterrows():
            categories = row["WC"]
            data.loc[data["WoScode"] == row["UT"], "wos_categories"] = categories
    return data


def add_WOSresearcharea(data: pd.DataFrame, wos_export: pd.DataFrame) -> pd.DataFrame:
    """Add the country of the affiliation of the first author, exported from Web of Science"""

    if "wos_researcharea" not in data.columns:
        for index, row in wos_export.iterrows():
            researcArea = row["SC"]
            data.loc[data["WoScode"] == row["UT"], "wos_researcharea"] = researcArea
    return data


def add_WOScitations(data: pd.DataFrame, wos_export: pd.DataFrame) -> pd.DataFrame:
    """Add the country of the affiliation of the first author, exported from Web of Science"""

    if "wos_citations" not in data.columns:
        for index, row in wos_export.iterrows():
            citations = row["NR"]
            citations_ref = row["CR"]
            data.loc[data["WoScode"] == row["UT"], "wos_citations"] = citations
            data.loc[data["WoScode"] == row["UT"], "wos_citation_refs"] = citations_ref
    return data


def add_WOSusage(data: pd.DataFrame, wos_export: pd.DataFrame) -> pd.DataFrame:
    """Add the country of the affiliation of the first author, exported from Web of Science"""

    if "wos_usage" not in data.columns:
        for index, row in wos_export.iterrows():
            citations = row["U2"]
            data.loc[data["WoScode"] == row["UT"], "wos_usage"] = citations
    return data
