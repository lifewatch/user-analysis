#import statements
import difflib
import pandas as pd
import numpy as np
import os
from difflib import SequenceMatcher
from pandas._testing import assert_index_equal
from pandas.api.types import is_string_dtype


class Standardizator:
    """
    Documentation should capture what this class is about. Mention mainly its responsibility and collaboration with others classes.
    """

    def __init__(self, pubfolder: str) -> pd.DataFrame:
        """
        constructor

        :param file: name of folder with publication info
        :type file: str
        :returns: dataframe object of publication files in folder
        :rtype: pd.DataFrame
        """
       
        dflist = []
        for filename in os.listdir(pubfolder):
            filedir = os.path.join(os.pardir, 'publication_data', filename)
            if filename.endswith('.xlsx') or filename.endswith('.xls'):
                dflist += [pd.read_excel(filedir)]
            elif filename.endswith('.csv'):
                dflist += [pd.read_csv(filedir)]
        
        # assert compatibility of dataframe headers
        series0 = dflist[0].columns
        for df in dflist:
            assert_index_equal(series0, df.columns)
            series0 = df.columns
            
        self.data = pd.concat(dflist)
       

    def add_WOSaffil(self, wos_export: str) -> pd.DataFrame:
        """
        This method adds affiliation information of the first author, exported from Web of Science, to a column 'wow_affil'    
        Note: other columns could be added aswell

        :param stand_file: folder with wos export files 
        :type stand_file: str  
        """

        self.data["wos_affil"] = np.nan
        for wos_file in os.listdir(wos_export):
            # Read data
            assert wos_file.endswith('.csv'), "Please make sure the wos_export is stored as a csv file"
            wos_file_dir = os.path.join(os.pardir,"wos_export", wos_file)
            export_data = pd.read_csv(wos_file_dir)            
            
            # 1. wos affiliation of first author | 'RP' = first author name & affiliation info ; 'RP_2' = first author affiliation info
            affil_firstauth = []
            for index, row in export_data['RP'].iteritems():
                affil_firstauth += [str(row).split('(corresponding author), ')[-1]]
            export_data['RP_2'] = affil_firstauth

            # 2. add wos_affil to data based on wos code | 'UT' = wos code
            for index, row in export_data.iterrows():
                self.data.loc[ self.data['WoScode'] == row['UT'], "wos_affil"] = row['RP_2']
        
        print("added wos affiliation to the pulication data")
        return self

    def exactMatch(self, stand_file: str) -> pd.DataFrame:
        """
        This method check for extact matches between standardized affiliation names and 'raw' affiliation names in the data (columns 'Affiliation' and 'wos_affil').
        In case of an exact match, the standardized affiliation name is added in the 'stand_affil' column.

        :param stand_file: standardized data file
        :type stand_file: str
        """

        ##TODO: FINISH!
        # Standardized information as dataframe:
        self.stand_data = pd.read_excel(stand_file, sheet_name='Affiliations_stand_LongList')
        print('Checking for an exact match between Affiliation names and standardized names from list')
        # Find exact matches & add standardized affiliation:
        for index, row in self.stand_data.iterrows():
            self.data.loc[ self.data['Affiliation'] == row['Institute'], ["stand_affil"]] = row['Institute standardized']

        return self


    def similarityMatch(self, stand_file: str) -> pd.DataFrame:
        """
        This method checks the similarity between standardized affiliation names and 'raw' affiliation names in the data (columns 'Affiliation' and 'wos_affil').
        In case of a similarity higher than ...%, the standardized affiliation name is added in the 'stand_affil' column.

        :param stand_file: standardized data file
        :type stand_file: str
        """
        
        """
        seq1 = self.data["Affiliation"]
        seq2 = self.stand_data["Institute standardized"]
        
        test1 = difflib.SequenceMatcher
        test1.set_seqs(seq1, seq2)
        test1.ratio()
        print(test1)
        """
        
        #TODO FINISH!
        
        difference = difflib.Differ()

        for index1, row1 in self.data.iterrows():
            seq1 = row1["Affiliation"]

            for index2, row2 in self.stand_data.iterrows():
                seq2 = row2["Institute standardized"]
                #print(seq1, seq2)

        return self

    def output(self, output_file: str) -> float:
        """
        This method writes the pd.Dataframe, with added standerdized information, to a new csv file

        :param outputCSV: file name of the output csv that will be generated
        :type outputCSV: str
        """

        if output_file.endswith('.xlsx')  or output_file.endswith('.xls'):
            self.data.to_excel(output_file)
            print("written to ", output_file)
        elif output_file.endswith('.csv'):
            self.data.to_csv(output_file)
            print("Data was written to ", output_file)
        else:
            print("unsupported data format")

        return self
        