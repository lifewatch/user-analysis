import pandas as pd
import os
import difflib
from pandas._testing import assert_index_equal

# all functions needed for Standardization and Labelling:


def load_folderdata(foldername):
    """this functions reads the data files in a folder (which are assumed to have the same tabular structure)
    and loads them into 1 dataframe."""

    folderdir = os.path.abspath(foldername)
    dflist = []
    for file in os.listdir(foldername):
        filename, file_extension = os.path.splitext(file)
        filedir = os.path.join(os.pardir, folderdir, file)

        # Load data files
        if file_extension == ".xlsx" or file_extension == ".xls":
            dflist += [pd.read_excel(filedir)]
        elif file_extension == ".csv":
            dflist += [pd.read_csv(filedir)]

    # Data file(s) as one dataframe
    series0 = dflist[0].columns
    for df in dflist:  # assert compatibility of dataframe headers
        assert_index_equal(series0, df.columns)
        series0 = df.columns
    data = pd.concat(dflist)

    return data


def load_filedata(filename):
    """this functions loads the specified data file as a pandas dataframe."""

    if str(filename).endswith(".xlsx") or str(filename).endswith(".xls"):
        stand_data = pd.read_excel(filename)
    elif str(filename).endswith(".csv"):
        stand_data = pd.read_csv(filename)

    return stand_data


def write_filedata(data: pd.DataFrame, filename: str):
    """this functions loads the specified data file as a pandas dataframe."""

    if str(filename).endswith(".xlsx") or str(filename).endswith(".xls"):
        data.to_excel(filename, encoding='utf8')
    elif str(filename).endswith(".csv"):
        data.to_csv(filename, encoding='utf8')

    return data


def update_datafile(data) -> float:
    """update file with standardized information"""

    # Check if dir exists
    outputdir = os.path.join(os.pardir, "standardized_data")
    outputfile = os.path.join(outputdir, "stand_data.csv")
    if not os.path.isdir(outputdir):
        os.mkdir(outputdir)
    # Output data
    data.to_csv(outputfile, index=False)


def best_standmatch(stand_file, affiliation):

    ratiolist = []
    standaffillist = []
    # Make list of non-stand affiliations where match ratio (between non stand and stand affil) > 0.8
    for index, row in stand_file.iterrows():
        affil_longstand = row["Institute"]
        affil_stand = row["Institute standardized"]

        diffobj = difflib.SequenceMatcher(None, affiliation, affil_longstand)
        if diffobj.ratio() > 0.8:
            ratiolist += [diffobj.ratio()]
            standaffillist += [affil_stand]

    # Select & return best candidate from list - Get the stand affil with highest match ratio
    if len(ratiolist) > 0:
        max_value = max(ratiolist)
        max_index = ratiolist.index(max_value)
        best_match = standaffillist[max_index]
    else:
        best_match = None
    #print("The best match is: ", best_match)
    return best_match
