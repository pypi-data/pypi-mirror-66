import math
import pandas as pd
from datetime import date
import numpy as np
import time

class Cleaner():
    # initialize filter object with pandas data frame
    def __init__(self, fish_df):
        self.fish_df = fish_df.copy() #pandas data frame copied to avoid pointer problems
        self.dirty_fish_id = [] #ids of fish with errors in its row
        self.dirty_fish = [] #all rows with errors
        self.dirty_idx = [] #idx of rows with errors (for quick look up and removal)

    #returns all of the erroneous rows found while cleaning the fish data
    def get_dirty_data(self):
        column_headers = ["FishID","Date", "TREND","Gear", "Species", "Sex", "Length",
                          "Mass", "Ktl", "Mass", "Maturity", "Age structure",
                          "stomach", "gonads", "fat_index", "parasite", "misc 1 text",
                          "misc 2 num", "misc 3 text", "misc 4 num", "Site", "KFL"]
        dirty_df = pd.DataFrame.from_records(self.dirty_fish)
        dirty_df.columns = column_headers

        return dirty_df

    #converts all categorical variable abbreviations (Species, Site, Gear, Sex) to upper case and removes white space
    def prep_data(self):
        self.fish_df['Species'] = self.fish_df['Species'].str.upper()
        self.fish_df['Site'] = self.fish_df['Site'].str.upper()
        self.fish_df['Gear'] = self.fish_df['Gear'].str.upper()
        self.fish_df['Sex'] = self.fish_df['Sex'].str.upper()
        self.fish_df['Species'] = self.fish_df['Species'].str.replace(" ", "")
        self.fish_df['Site'] = self.fish_df['Site'].str.replace(" ", "")
        self.fish_df['Gear'] = self.fish_df['Gear'].str.replace(" ", "")
        self.fish_df['Sex'] = self.fish_df['Sex'].str.replace(" ", "")

    #cleans the fish data based on the booleans indicating which columns should be checked for errors
    def clean_fish_data(self, date = True, mass = True, length = True, species = True,
                        site = True, gear = True, sex = True):
        self.prep_data()

        for i in self.fish_df.index:
            try:
                if date:
                    self.check_date(i)
                if mass:
                    self.check_mass(i)
                if length:
                    self.check_length(i)
                if species:
                    self.check_species(i)
                if site:
                    self.check_site(i)
                if gear:
                    self.check_gear(i)
                if sex:
                    self.check_sex(i)

            except: #catches the errors thrown by individual cleaning functions and adds those rows to error lists
                self.dirty_fish_id.append(self.fish_df["FishID"][i])
                self.dirty_fish.append(list(self.fish_df.iloc[i,]))
                self.dirty_idx.append(i)

        # print(self.dirty_fish_id)
        # print(pd.DataFrame.from_records(self.dirty_fish))
        # print(len(self.dirty_idx))
        # self.fish_df.replace(0, np.nan, inplace=True)
        return self.fish_df.drop(self.dirty_idx)

    #checks to make sure there are no date errors at index i
    def check_date(self, i):
        cur_year = date.today().year
        date_caught = self.fish_df["Date"][i]

        day = date_caught.day
        month = date_caught.month
        year = date_caught.year

        if (year < 1962) or (year > cur_year):#there shouldn't be any records before filling of lake and today's date
            raise ValueError('Year not in range: ', year)
        elif (month < 1) or (month > 12):
            raise ValueError('Month not in range: ', month)
        elif (day < 1) or (day > 31):#not a robust check, but should be sufficient
            raise ValueError('Day not in range: ', day)

    #checks to make sure there are no species abreviation errors at index i
    def check_species(self, i):
        species = self.fish_df["Species"][i]
        valid_species = ["GSF", "STB", "BGL", "SMB", "LMB", "WAE", "GZD", "BLC",
                        "CCF", "TFS", "CRP", "RSH", "YBH", "RBT", "FMS", "BLG",
                        "RZB", "WTC", "OTH"]

        if species not in valid_species:
            raise ValueError('Invalid species: ', species)

    #checks to make sure there are no gear abreviation errors at index i
    def check_gear(self, i):
        gear = self.fish_df["Gear"][i]
        valid_gear = ["GN", "EL", "AN", "CR", "SN"]

        if gear not in valid_gear:
            raise ValueError('Invalid gear: ', gear)

    #checks to make sure there are no sex abreviation errors at index i
    def check_sex(self, i):
        sex = self.fish_df["Sex"][i]
        valid_sexes = ["U", "F", "M"]

        if (sex not in valid_sexes) and (not np.isnan(sex)):
            raise ValueError('Invalid sex: ', sex)

    #checks to make sure fish at length index i, if recorded, is not a negative number
    def check_length(self, i):
        length = self.fish_df["Length"][i]

        if not math.isnan(length):
            if length < 0:
                raise ValueError('Invalid length (< 0): ', length)

    #checks to make sure fish mass at index i, if recorded, is not a negative number
    def check_mass(self, i):
        mass = self.fish_df["Mass"][i]

        if not math.isnan(mass):
            if mass < 0:
                raise ValueError('Invalid mass (< 0): ', mass)

    #checks to make sure there are no site abreviation errors at index i
    def check_site(self, i):
        site = self.fish_df["Site"][i]
        #these were ones given by Alexandria
        # valid_site = ['GH', 'WW', 'SJ', 'BF', 'PB', 'RN', 'WC', 'AT', 'HA','NW',
        #                 'HC', 'CR', 'GB', 'DM', 'LC', 'NK', 'AI', 'RC', 'HI', 'KC']
        #these were ones with frequences high enough to probably be real
        valid_site = ["GH", "RN", "SJ", "WW", "BF", "PB", "KC", "NW", "HA",
                            "PF", "HC", "WC", "CC", "SC", "DM"]

        if site not in valid_site:
            raise ValueError('Invalid site: ', site)
