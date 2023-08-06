import pandas as pd
import numpy as np
from .download import *
from .cleaner import *
from .join import range_join, join_by_month_or_year


class Data():
    def __init__(self):
        #Download the data
        self.download()
        ts2 = time.time()
        #initialize a dictionary or somthing to hold dataframes
        self.dataframes = {}
        #+++++++++++++++++++++++++++++++++++++++++++get and parse the fish data ++++++++++++++++++++++++++++++++++++++++++++++++++
        download_msg = "Cleaning fish data . . ."
        print(download_msg, end='\r')
        fish_data_path = "lakepowell/data/fish_data"
        #build the fish data parsar
        fish_df = pd.read_excel(get_fishdata_path())
        column_headers = ["FishID","Date", "TREND","Gear", "Species", "Sex", "Length",
                          "Mass", "Ktl", "Relative Weight", "Maturity", "Age structure",
                          "stomach", "gonads", "fat_index", "parasite", "misc 1 text",
                          "misc 2 num", "misc 3 text", "misc 4 num", "Site", "KFL"]

        fish_df.columns = column_headers

        #clean fish data
        clean = Cleaner(fish_df)
        fish_df = clean.clean_fish_data() #all clean values default to true
        # print(clean.get_dirty_data())

        #split fish data date into Day, Month, Year columns
        fish_df['Day'] = pd.DatetimeIndex(fish_df['Date']).day
        fish_df['Month'] = pd.DatetimeIndex(fish_df['Date']).month
        fish_df['Year'] = pd.DatetimeIndex(fish_df['Date']).year

        #Categorize fish data into UP and LO lakepowell
        site_loc = {'GH':'UP', 'WW':'LO', 'SJ':'UP', 'BF':'UP', 'PB':'LO',
                        'RN':'UP', 'WC':'LO', 'AT':'LO', 'HA':'UP','NW':'LO',
                        'HC':'UP', 'CR':'LO', 'GB':'UP', 'DM':'LO', 'LC':'LO',
                        'NK':'UP', 'AI':'LO', 'RC':'UP', 'HI':'UP', 'KC':'UP'}
        fish_df['Location']= fish_df['Site'].map(site_loc)

        self.dataframes["fish_data"] = fish_df

        print(" " * len(download_msg), end='\r') # Erase the loading message


        #++++++++++++++++++++++++++++++++++++++++++get and parse the water data +++++++++++++++++++++++++++++++++++++++++++++++++++++
        download_msg = "Cleaning water data . . ."
        print(download_msg, end='\r')
        water_data_path =  "lakepowell/data/water_data"
        water_df = pd.read_csv(get_waterdata_path())

        new = water_df["DATE MEASURED"].str.split(r",\s|\s", n = 3, expand = True)

        #------------------- convert month to digit -------------------
        months = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6,
                    'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
        df_months = new[1]
        for i in range(0, len(df_months)):
            df_months[i] = months.get(df_months[i])
        #--------------------------------------------------------------

        water_df["MONTH"]= df_months.astype(int)
        water_df["DAY"]= new[2].astype(int)
        water_df["YEAR"]= new[3].astype(int)

        self.dataframes['water_data'] = water_df
        print(" " * len(download_msg), end='\r') # Erase the loading message


    def download(self):
        download_msg = "Downloading fish data . . ."
        print(download_msg, end='\r')
        fish_data_path = download_fish_file()
        print(" " * len(download_msg), end='\r') # Erase the downloading message

        download_msg = "Downloading water data . . ."
        water_data_path = download_water_data()
        print(" " * len(download_msg), end='\r') # Erase the downloading message


    def get_fish_data(self):
        return self.dataframes["fish_data"]

    def get_water_data(self):
        return self.dataframes["water_data"]

    def join_by_range(self, fish_data, water_data, spread, operation):
        df = range_join(fish_data, water_data, spread, operation)
        return df

    def join_by_year(self, fish_data, water_data):
        df = join_by_month_or_year(fish_data, water_data, time_unit="year")
        return df

    def join_by_month(self, fish_data, water_data):
        df = join_by_month_or_year(fish_data, water_data, time_unit="month")
        return df
    
    def find_abrv(self, key):
        common_names =  {"BLG": "Bluegill Sunfish",
                   "GSF": "Green Sunfish", 
                   "STB": "Striped Bass", 
                   "SMB": "Smallmouth Bass", 
                   "LMB": "Largemouth Bass", 
                   "WAE": "Walleye",  
                   "BLC": "Black Crappie",
                   "CCF": "Channel Catfish", 
                   "TFS": "Threadfin Shad",
                   "GZD": "Gizzard Shad", 
                   "CRP": "Common Carp?", 
                   "RBT": "Rainbow Trout", 
                   "OTH": "Other?",
                   "RZB": "Razorback Sucker??", 
                   "YBH": "Yellow Bullhead Carp????",
                   "FMS": "FMS", 
                   "RSH": "RSH",  
                   "WTC": "WTC", 
                   "BGL": "More Blue Gill??????"}

        sci_names={"BLG": "Lepomis macrochirus",
                   "GSF": "Lepomis cyanellus", 
                   "STB": "Morone saxatilis", 
                   "SMB": "Micropterus dolomieu", 
                   "LMB": "Micropterus salmoides", 
                   "WAE": "Sander vitreus",  
                   "BLC": "Pomoxis nigromaculatus",
                   "CCF": "Ictalurus punctatus", 
                   "TFS": "Dorosoma petenense",
                   "GZD": "Dorosoma cepedianum", 
                   "CRP": "Cyprinus carpio", 
                   "RBT": "Oncorhynchus mykiss", 
                   "OTH": "Other?",
                   "RZB": "Xyrauchen texanus", 
                   "YBH": "Ameiurus natalis ",
                   "FMS": "FMS", 
                   "RSH": "RSH",  
                   "WTC": "WTC", 
                   "BGL": "More Lepomis macrochirus??????"}

        Gear_abv = {"EL": "Electrofishing",
            "GN":"Gill-nets",
            "AN": "AN",
            "CR": "CR",
            "SN": "SN",
            "GH": "Gill-net miss-type??",
            "BN": "Gill-net miss-type?",
            "FL": "FL",
            "SJ":"SJ",
            "GM":"Gill-net miss-type?",
            "ERL":"Electrofishign miss-type?",
            "GB":"Gill-net miss-type?",
            "GBN":"Gill-net miss-type?",
            "125":"125",
            "EEL":"Electrofishing miss-type?",
            "El;": "Electrofishing miss-type?"}

        Site_abv = {"GH": "Good Hope",
            "QC":"QC",
            "FC":"Farley Canyon",
            "G":"G",
            "GD":"GD",
            "RH":"RH",
            "SA":"SA",
            "RP":"RP",
            "AL":"AL",
            "ES":"Escalante",
            "U":"U",
            "RN": "Rincon",
            "SJ": "San Juan",
            "WW": "Wahweap",
            "BF": "BullFrog",
            "PB": "Padre Bay",
            "KC":"Knoll Canyon",
            "NW": "Norther Wahweap",
            "HA": "Halls",
            "PF": "PF",
            "HC":"Halls Creek/ Halls Crossing",
            "WC":"Warm Creek",
            "CC": "Castle Creek/ Coper Canyon",
            "SC":"Stanton Creek",
            "DM":"Dangling Rope Marina",
            "HI":"Hite",
            "LC":"Last Chance",
            "NC":"Navajo Canyon",
            "EM":"EM",
            "AT": "Antelope",
            "FD":"FD",
            "GB":"Good Hope Bay",
            "GP":"GP",
            "RC":"Red Canyon",
            "GC":"Glen Canyon",
            "CR":"Castle Rock",
            "NK":"Neskahi",
            "S":"Stateline",
            "NV":"Navajo Canyon",
            "GG":"GG",
            "QN":"QN",
            "GN":"GN",
            "EL":"EL"}
        #edge case if it's in dictionary or not
        size = len(key)
        
        if size == 3 and key in common_names:
            #look in species
            C_name = "Common Name is: " + common_names[key]
            S_name = "Scientific Name is: " + sci_names[key]
            return(C_name, S_name)
        elif size ==2:
            #look in gear/ location
            G_Type = "Gear Used is: "
            Site = "Site is: "
            if key in Gear_abv and key in Site_abv:
                G_Type = G_Type + Gear_abv[key]
                Site = Site + Site_abv[key]
                return(G_Type, Site)
            elif key in Gear_abv:
                G_Type = G_Type + Gear_abv[key]
                return(G_Type)
            elif key in Site_abv:
                Site = Site + Site_abv[key]
                return(Site)
            else:
                return("Error, Invalid Abriviation")
        
        return("Error, Invalid Abriviation")


            
        
