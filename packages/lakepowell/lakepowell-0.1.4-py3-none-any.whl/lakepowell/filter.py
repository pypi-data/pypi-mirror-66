import pandas as pd

class Filter:
    # initialize filter object with pandas data frame
    def __init__(self, df):
        self.df = df.copy() #pandas data frame copied to avoid pointer problems

    # select columns of interest by name
    # @Param cols: list of type string column names to be included in the new dataframe
    def selectColumns(self, cols):
        self.df = self.df[cols]

    #filter based on gear values in given list
    # @Param gear: list of type string gear names to be included in the new dataframe
    def givenGear(self, gear):
        self.df = self.df[self.df.Gear.isin(gear)]

    #filter based on species values in given list
    # @Param species: list of type string species names to be included in the new dataframe
    def givenSpecies(self, species):
        self.df = self.df[self.df.Species.isin(species)]

    #Only includes fish that have the given male or female distinction
    # @Param male: boolean for whether males should be included or not
    # @Param male: boolean for whether females should be included or not
    def givenSexes(self, male, female):
        if male and female: #all data with Male or Female distinction
            self.df = self.df[self.df.Sex == "M" or self.df.Sex == "F"]
        elif male and not female: #only males
            self.df = self.df[self.df.Sex == "M"]
        elif not male and female: #only females
            self.df = self.df[self.df.Sex == "F"]

    #filter based on site values in given list
    # @Param sites: list of type string site names to be included in the new dataframe
    def givenSites(self, sites):
        self.df = self.df[self.df.Site.isin(sites)]

    #returns fish that are in the length range of low (inclusive) to high (inclusive)
    # @Param low: fish must be greater or equal to this value
    # @Param high: fish must be less than or equal to this value
    def rangeLength(self, low, high):
        self.df = self.df[self.df.Length >= low]
        self.df = self.df[self.df.Length <= high]

    #returns fish that are in the mass range of low (inclusive) to high (inclusive)
    # @Param low: fish must be greater or equal to this value
    # @Param high: fish must be less than or equal to this value
    def rangeMass(self, low, high):
        self.df = self.df[self.df.Mass >= low]
        self.df = self.df[self.df.Mass <= high]

    #returns fish that are in the KTL range of low (inclusive) to high (inclusive)
    # @Param low: fish must be greater or equal to this value
    # @Param high: fish must be less than or equal to this value
    def rangeKtl(self, low, high):
        self.df = self.df[self.df.Ktl >= low]
        self.df = self.df[self.df.Ktl <= high]

    #returns fish that are caught from year1 (inclusive) and year2 (inclusive)
    # @Param year1: fish must be caught after or during this year (type integer)
    # @Param year2: fish must be caught before or during this year (type integer)
    def rangeYears(self, year1, year2):
        self.df = self.df[self.df.Year >= year1]
        self.df = self.df[self.df.Year <= year2]

    #returns fish that are caught from month1 (inclusive) and month2 (inclusive) in any year
    # @Param year1: fish must be caught after or during this month (type integer)
    # @Param year2: fish must be caught before or during this month (type integer)
    def rangeMonths(self, month1, month2):
        self.df = self.df[self.df.Month >= month1]
        self.df = self.df[self.df.Month <= month2]

    #returns fish that are caught from day1 (inclusive) and day2 (inclusive) in any month
    # @Param year1: fish must be caught after or during this day (type integer)
    # @Param year2: fish must be caught before or during this day (type integer)
    def rangeDays(self, day1, day2):
        self.df = self.df[self.df.Day >= day1]
        self.df = self.df[self.df.Day <= day2]

    #filter rows only between the given dates - will work with bad dates as long
    #as they are numbers
    # @Param d1: fish must be caught after or during this day (type integer)
    # @Param m1: fish must be caught after or during this month (type integer)
    # @Param y1: fish must be caught after or during this year (type integer)
    # @Param d2: fish must be caught before or during this day (type integer)
    # @Param m2: fish must be caught after or during this month (type integer)
    # @Param y2: fish must be caught after or during this year (type integer)
    def betweenDates(self, d1, m1, y1, d2, m2, y2):
        self.rangeYears(y1, y2)
        self.df = self.df[(self.df.Month >= m1) & (self.df.Day >= d1)]
        self.df = self.df[(self.df.Month <= m2) & (self.df.Day <= d2)]

    #filter based on month values in given list
    # @Param month: list of type integer of months to be included in the new dataframe
    def givenMonths(self, months):
        self.df = self.df[self.df.Month.isin(months)]

    #filter based on year values in given list
    # @Param month: list of type integer of years to be included in the new dataframe
    def givenYears(self, years):
        self.df = self.df[self.df.Year.isin(years)]
