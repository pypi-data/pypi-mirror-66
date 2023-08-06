import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import lakepowell
from scipy.stats.stats import pearsonr


class Operations():

########Summarize functions ###########
    def table_summary(df, layers, feature, calcs, titles):
        '''
        Summarizes fish or lake data based on given criteria over a specified numerical variable.

        Parameters:
            layers (list): An ordered list of column header names (strings). First layer in the list is the largest group and the last is the smallest subgrouping.
            feature (string): is the name of the numerical variable column that should have a summary calculation performed over it.
            calcs (string): are the different calculations to be made over the feature.

        Returns: (DataFrame) Summarized table
        '''
        if feature is None: #if the feature is None, assume they want to count the lowest subgrouping
            feature = layers[-1]
            calcs = ['count']
        if calcs is None: #if there is no calculation assume they want to count the feature
            calcs = ['count']
        if len(calcs) != len(titles): #catch errors in length of given title and replace with numbered list
            titles = map(str, range(len(calcs) + 1))

        grouped_multiple = df.groupby(layers).agg({feature: calcs})
        grouped_multiple.columns = titles
        grouped_multiple = grouped_multiple.reset_index()

        return grouped_multiple


    def join_fish_and_water(fish_df, water_df):
        '''
        Combines the fish and lake condition data tables based on date. It will join off of the most specific date in both dataframes.
        Parameters:
            fish_df (dataframe): the fish data pandas dataframe
            water_df (dataframe): the lake conditions pandas dataframe
        '''
        year = False
        month = False
        day = False
        new_df = None

        fish_df.columns = ["Fish_" + s for s in fish_df.columns] #add "Fish_" to the start of every string
        water_df.columns = ["Lake_" + s for s in water_df.columns] #add "Lake_" to the start of every string

        if "Fish_Year" in fish_df.columns and "Lake_YEAR" in water_df.columns:
            year = True
        if "Lake_Month" in fish_df.columns and "Lake_MONTH" in water_df.columns:
            month = True
        if "Lake_Day" in fish_df.columns and "Lake_DAY" in water_df.columns:
            day = True

        #join based on most specific date in the given dataframes
        if year and month and day:
            new_df = pd.merge(fish_df, water_df,  how='left', left_on=["Fish_Year","Fish_Month","Fish_Day"],
                                right_on = ["Lake_YEAR", "Lake_MONTH", "Lake_DAY"])
            new_df = new_df.drop(["Lake_YEAR", "Lake_MONTH", "Lake_DAY"], axis = 1)
        elif year and month and not day:
            new_df = pd.merge(fish_df, water_df,  how='left', left_on=["Fish_Year", "Fish_Month"],
                                right_on = ["Lake_YEAR", "Lake_MONTH"])
            new_df = new_df.drop(["Lake_YEAR", "Lake_MONTH"], axis = 1)
        elif year and not month and not day:
            new_df = pd.merge(fish_df, water_df,  how='left', left_on=["Fish_Year"],
                                right_on = ["Lake_YEAR"])
            new_df = new_df.drop(["Lake_YEAR"], axis = 1)

        return new_df


    def cpue_scale(fish_df, full_fish_df):
        '''
        Calculates the CPUE by determining the CPUE for each trip and then scales EL to GN to give a more accurate representation of CPUE.
        Parameters:
            fish_df (dataframe): the fish dataframe subset to calculate CPUE across
            full_fish_df(dataframe): the entire fish dataframe to use as a reference in determining EL to GN ratio
        '''
        titles = ['CPUE']
        layers = ['Species', 'Year', 'Location', 'Month', 'Site', 'Gear']
        feature = 'Length'
        calcs = ['count']
        ratio = get_el_ratio(full_fish_df)

        gear_count = table_summary(fish_df, layers, feature, calcs, ['count'])
        gear_count['CPUE'] = gear_count['count'].divide(8) #4 nets for two nights for each trip for CPUE
        gear_count.loc[gear_count.Gear == 'EL', 'CPUE'] = gear_count.loc[gear_count.Gear == 'EL', 'CPUE'] / ratio #scale CPUE for EL
        year_cpue = table_summary(gear_count, ['Species', 'Year', 'Location'], 'CPUE', ['mean'], ['mean']) #mean gives CPUE for Year

        return year_cpue


    def cpue_precise(fish_df):
        '''
        Calculates the CPUE by determining the CPUE for each trip
        Parameters:
            fish_df (dataframe): the fish dataframe subset to calculate CPUE across
        '''
        titles = ['count']
        layers = ['Species', 'Year', 'Location', 'Month', 'Site']
        feature = 'Length'
        calcs = ['count']

        site_count = table_summary(fish_df, layers, feature, calcs, ['count']) #count the fish cought for each colection
        site_count['CPUE'] = site_count['count'].divide(8) #calculate CPUE for each site
        year_cpue = table_summary(site_count, ['Species', 'Year', 'Location'], 'CPUE', ['mean'], ['mean']) #calculate CPUE across year/location

        return year_cpue


    def cpue_simple(fish_df):
        '''
        Calculates the CPUE by determining the CPUE across each year, assuming that 4 trips were made each year_cpue and all gear types performed equally well
        Parameters:
            fish_df: the fish dataframe subset to calculate CPUE across
        '''
        titles = ['CPUE']
        layers = ['Species', 'Year', 'Location']
        feature = 'Length'
        calcs = [lambda x: len(x)/32]#divide catch by 32 = 4 nets * 2 nights * 4 trips in a year

        loc_cpue = table_summary(fish_df, layers, feature, calcs, titles)
        return loc_cpue


    def get_el_ratio(fish_df):
        '''
        Determines the ratio of fish caught with EL to fish caught with GN (EL/GN)
        Parameters
            fish_df: the entire fish dataframe to use as a reference in determining EL to GN ratio
        '''
        layers = ['Year', 'Location', 'Site', 'Month', 'Day', 'Gear']
        feature = 'Length'
        calcs = ['count']

        year_gear_counts = table_summary(fish_df, layers, feature, calcs, ['num_fish'])
        gear_means = table_summary(year_gear_counts, ['Gear'], 'num_fish', ['mean'], ['Mean'])
        el = gear_means.loc[gear_means['Gear'] == 'EL', 'Mean'].iloc[0]
        gn = gear_means.loc[gear_means['Gear'] == 'GN', 'Mean'].iloc[0]
        el_ratio = el/gn

        return el_ratio

###########Correltation Functions##############

    def summarize_cpue(species, biotic, timeframe, auto):
      """
      Generates the Catch per Unit Effort (CPUE).

      Parameters:
        species (str): The three letter acronym for the species of interest.
        biotic (str): One of the five options for understanding the amount of fish caught. ('individual', 'ave_len', 'tot_len, 'ave_mass', or 'tot_mass'
        timeframe (str): The period over which the data should be summarized. ('year' or 'month')
      Returns:
        (Dataframe) This function returns a panda (sometimes multilevel) with one column, the CPUE.
      """
      fish_data = data.get_fish_data()
      species_df = fish_data[fish_data['Species'] == species]
      allowed_weight_species= ['LMB', 'STB']  # List of which Species have mass data
      summarized = None
      if biotic.lower() == 'individual':
        # Count the number of fish caught and assign it to 'Catch'
        summarized = species_df.groupby(['Year', 'Month', 'Day']).agg({'FishID':'count', 'Site': 'unique'})
        summarized.rename(columns={"FishID": "Catch"}, inplace = True)
      elif biotic == 'ave_len':
        # Average the length of fish caught and assign it to 'Catch'
        summarized = species_df.groupby(['Year', 'Month', 'Day']).agg({'FishID':'count', 'Length':'mean', 'Site': 'unique'})
        summarized.rename(columns={"Length": "Catch"}, inplace = True)
      elif biotic == 'tot_len':
        # Sum the length of fish caught and assign it to 'Catch'
        summarized = species_df.groupby(['Year', 'Month', 'Day']).agg({'FishID':'count', 'Length':'sum', 'Site': 'unique'})
        summarized.rename(columns={"Length": "Catch"}, inplace = True)
      elif (biotic == 'ave_mass') | (biotic == 'tot_mass'):
        # Check that the species is valid and warn the user of imputation
        if species not in allowed_weight_species: #caviot on speices
          print("Error: Mass not avalible for ", species)
          return None

        if not auto:
          print("WARNING: Insuficient recorded mass data, some masses are imputed.")
          response = input("Do you want to Continue? (y/n)")
        else:
          response = 'y'

        if response.lower() == 'y':
          if biotic == 'ave_mass':
            # Average the mass of fish caught and assign it to 'Catch'
            summarized = species_df.groupby(['Year', 'Month', 'Day']).agg({'FishID':'count', 'Mass':'mean', 'Site': 'unique'})
            summarized.rename(columns={"Mass": "Catch"}, inplace = True)
          elif biotic == 'tot_mass':
            # Sum the mass of fish caught and assign it to 'Catch'
            summarized = species_df.groupby(['Year', 'Month', 'Day']).agg({'FishID':'count', 'Mass':'sum', 'Site': 'unique'})
            summarized.rename(columns={"Mass": "Catch"}, inplace = True)
        else:
          return None
      else:
        print("Error: Invalid Biotic Factor")
        return None

      CPUE = None
      if timeframe.lower() == "year":
        catch_inYear = summarized["Catch"].groupby(level = 0).sum()
            # The sum of the biotic factor in "Catch" for the year

        unit_effort = summarized['Site'].map(lambda Site: len(Site)).groupby(level = 0).sum()
            # The sum of the days spent a each site visited in the year. If site A appeared
            # on 5 entries over days 1, 2, and 4 and site B appeared on 27 entries on days 2 and 3
            # the unit effort would be 5: three days at site A and 2 days at site B

        CPUE = catch_inYear/unit_effort
      elif timeframe.lower() == "month":
        catch_inMonth = summarized["Catch"].groupby(level = (0, 1)).sum()
            # The sum of the biotic factor in "Catch" for the year

        unit_effort = summarized['Site'].map(lambda Site: len(Site)).groupby(level = (0, 1)).sum()
            # The sum of the days spent a each site visited in the month. If site A appeared
            # on 5 entries over days 1, 2, and 4 and site B appeared on 27 entries on days 2 and 3
            # the unit effort would be 5: three days at site A and 2 days at site B

        CPUE = catch_inMonth/unit_effort
      elif timeframe.lower() == "days": #Not Ready Yet
        pass
      else:
        print("Error: Invalid Timeframe")
        return None

      return pd.DataFrame(CPUE, columns =['CPUE'])

    def summarize_water(abiotic, timeframe):
      """
      Summarizes water data.

      Parameters:
        abiotic (str): The abbreviation indicating the desired method for measuring "What is the water like" ('diff_level', 'max_level', 'min_level', 'ave_level', 'max_temp', or 'min_temp')
        timeframe (str): The period over which the data should be summarized. ('year' or 'month')
      Returns:
        (Dataframe) This function returns water data grouped into functional spans of time based on 'timeframe' in a dataframe.
      """

      water_data = data.get_water_data()
      levels = None
        # Set the depth at which to group the water data based on 'timeframe'
      if timeframe.lower() == 'year':
        levels = ['YEAR']
      elif timeframe.lower() == 'month':
        levels = ['YEAR', 'MONTH']
      else:
        print("ERROR: Invalid timeframe")
        return None
        # Actually group the water data and pull the abiotic factor of interest
      if abiotic == 'diff_level':
        water_data = water_data.groupby(levels).agg({'ELEVATION':np.ptp})
        water_data.rename(columns={'ELEVATION': "Abiotic"}, inplace = True)
      elif abiotic == 'max_level':
        water_data = water_data.groupby(levels).agg({'ELEVATION':'max'})
        water_data.rename(columns={'ELEVATION': "Abiotic"}, inplace = True)
      elif abiotic == 'min_level':
        water_data = water_data.groupby(levels).agg({'ELEVATION':'min'})
        water_data.rename(columns={'ELEVATION': "Abiotic"}, inplace = True)
      elif abiotic == 'ave_level':
        water_data = water_data.groupby(levels).agg({'ELEVATION':'mean'})
        water_data.rename(columns={'ELEVATION': "Abiotic"}, inplace = True)
      elif abiotic == 'max_temp':
        water_data = water_data.groupby(levels).agg({'HIGH TEMP':'max'})
        water_data.rename(columns={'HIGH TEMP': "Abiotic"}, inplace = True)
      elif abiotic == 'min_temp':
        water_data = water_data.groupby(levels).agg({'LOW TEMP':'min'})
        water_data.rename(columns={'LOW TEMP': "Abiotic"}, inplace = True)
      else:
        print('ERROR: Invalid abiotic factor')
        return None

      return water_data

    def abiotic_biotic_corr(species, biotic, abiotic, timeframe = 'year', lag_years = [0,1,2,3,4,5,10], auto = False):
      """
      Calculate's Pearson's R for correlations between the biotic data with the abiotic data from previous years.

      Parameters:
        species (str): The three letter acronym for the species of interest.
        biotic (str): One of the five options for understanding the amount of fish caught. ('individual', 'ave_len', 'tot_len, 'ave_mass', or 'tot_mass'
        abiotic (str): The abbreviation indicating the desired method for measuring "What is the water like" ('diff_level', 'max_level', 'min_level', 'ave_level', 'max_temp', or 'min_temp')
        timeframe (str): The period over which the data should be summarized. ('year' or 'month')
        lag_years (list(int)): the list of which delays (in years) might have significant impact on the biotic measure
      Returns:
        (Dataframe) A pearson correlation table with pandas.dataframe.corr. The first column is the only one of interest as it compares the biologic data with abiotic data from that year and previous years.
      """

      import pandas as pd
      # TODO check on species
      # TODO check on biotic factor

      catch_per_unit_effort = summarize_cpue(species, biotic, timeframe, auto)
      water_summary = summarize_water(abiotic, timeframe)

      if timeframe.lower() == 'year':
        joined = catch_per_unit_effort.join(water_summary)

        abio_data = water_summary['Abiotic']

          # Create a shifted column of water data for each of the lag years
        lagged_df = pd.DataFrame()
        for lag in lag_years:
            col_name = "-"+str(lag)+" years"
            lagged_df[col_name] = water_summary['Abiotic'].shift(periods = lag)

        joined_w_lag = pd.concat([joined, lagged_df], axis =1)
            # Append the data from the previous years to the joined data frame so that the
            # fish abbundace can be compared to previous years water

          # perform the correlation and return
        return joined_w_lag.corr('pearson')
      elif timeframe.lower() == 'month':
        # Gives the CPUE and water dat for each month trips occured in.
        # Currently, lags show the water data from the same month the indicated number of years previously
        joined = catch_per_unit_effort.reset_index().join(water_summary,on=['Year','Month']).set_index(catch_per_unit_effort.index.names)

        abio_data = water_summary['Abiotic']

          # Create a shifted column of water data for each of the lag years (but a period is a month, so *12)
        lagged_df = pd.DataFrame()
        for lag in lag_years:
            col_name = "-"+str(lag)+" years"
            lagged_df[col_name] = water_summary['Abiotic'].shift(periods = lag*12)

        joined_w_lag = pd.concat([joined, lagged_df], axis =1)
            # Append the data from the previous years to the joined data frame so that the
            # fish abbundace can be compared to previous years water

          # perform the correlation and return
        return joined_w_lag.corr('pearson')

    #########################Filter Functions#####################################
    def conditional_range(df, con_col, con_var, num_col, min, max):
        """
        Filters specific ranges of numerical variables based on categorical variables in the data set.

        Parameters:
            df (Pandas.DataFrame): The dataframe to be filtered.
            con_col (str): The categorical column in the dataframe that contains the conditional variable.
            con_var (str): The condition variable found in the categorical column that you want to filter based on.
            num_col (str): The numerical column that you are going to filter between the min and max for the given condition.
            min (str): The minimum acceptable value of the numerical column for the conditional variable.
            max (str): The maximum acceptable value of the numerical column for the conditional variable.
        Returns:
            (Dataframe) The new filtered dataframe.
        """
        for index,row in df.iterrows():
            if row[con_col] == con_var:
                if not (row[num_col] >= min) and not(row[num_col] <= max):
                    df.drop(index, inplace=True)

    def betweenDates(df, d1, m1, y1, d2, m2, y2):
        """
        Filters out all data that is not between the given dates

        Parameters:
            df (Pandas.DataFrame): The dataframe to be filtered.
            d1 (int): Day of start date.
            m1 (int): Month of start date.
            y1 (int): Year of start date.
            d2 (int): Day of end date.
            m2 (int): Month of end date.
            y2 (int): Year of end date.
        Returns:
            (Dataframe) The new filtered data frame.
        """
        df = df[(df.Year >= y1) & (df.Year <= y2)]
        df = df[(df.Month >= m1) & (df.Day >= d1)]
        df = df[(df.Month <= m2) & (df.Day <= d2)]

    ############################New CPUE Functions###################################
    def collec_fish_count(self, fish_df):
        """
        Subgroups the fish dataframe into collections and counts the fish caught in each of those collections.

        Parameters:
            fish_df (Pandas.DataFrame): The fish dataframe to count trips in. Must have the following columns: 'Year', 'Location', 'Site', 'Gear', 'Month', 'Day'.
        Returns:
            (Dataframe) The fish dataframe summarized by collection with the number of fish caught each collection.
        """
        layers = ['Year', 'Location', 'Site', 'Gear', 'Month', 'Day']
        feature = 'Length'
        calcs = ['count']
        titles = ['Fish Count']

        grouped_multiple = fish_df.groupby(layers).agg({feature: calcs})
        grouped_multiple.columns = titles
        grouped_multiple = grouped_multiple.reset_index()

        fish_sum = grouped_multiple
        fish_sum = fish_sum[fish_sum['Gear'].isin(['EL', 'GN'])]
        return fish_sum

    #Assign trip ids that are connected to the previus trip by the buffer of days
    def assign_trip_ids(self, fish_sum, buffer):
        """
        Assigns a column of trips to a summary collection dataframe as produced by collec_fish_count()

        Parameters:
            fish_sum (Pandas.DataFrame): The fish dataframe summarized by collections. Must have the following columns: 'Year', 'Location', 'Site', 'Gear', 'Month', 'Day'.
            buffer (int): The number of days that can occur between collections while still including them in the same trip.
        Returns:
            (Dataframe) The fish collection summary table with addition of columns ids for each trip and a column that numbers the collections in each trip.
        """
        trip_id = 0
        collec_num = 1
        next_month = {1:2, 2:3, 3:4, 4:5, 6:7, 7:8, 8:9, 10:11, 11:12, 12:1}
        #29 is used for february because worst case it increases the buffer across the end of a month on a non leap year.
        days_in_month = {1:31, 2:29, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
        row_ids = []
        collec_of_trips = []

        #loop through each collection in the fish summary table
        for i in range(0, len(fish_sum)):
            row = fish_sum.iloc[i]

            if i == 0: #the first item in the table doesn't have a previous day to check
                trip_id = trip_id + 1
                row_ids.append(trip_id)
                collec_of_trips.append(collec_num) #collection number in the trip is 1 because it is the first item

            elif row['Gear'] == 'EL': #EL trips occur across a single collection
                trip_id = trip_id + 1
                row_ids.append(trip_id)
                collec_num = 1 #collection number in the trip is 1 because it is the only one in the trip
                collec_of_trips.append(collec_num)

            elif row['Gear'] == 'GN': #GN collection need to see if it is connect to the previous collection as part of the same trip
                prev_trip = fish_sum.iloc[i - 1]

                if(prev_trip['Year'] == row ['Year'] and (prev_trip['Location'] == row ['Location'])
                    and prev_trip['Site'] == row ['Site'] and prev_trip['Gear'] == row ['Gear'] ): #share the same trip info but collection was performed on a differnt day

                    if prev_trip['Month'] == row ['Month']:
                        day_range = list(range(int(prev_trip['Day']), int(prev_trip['Day'])+buffer+1)) #range of days that are valid to be included in the same trip

                        if row['Day'] in day_range: #is in the same trip
                            row_ids.append(trip_id) #use the same trip id
                            collec_num = collec_num + 1 #increment collection number in the trip because it is part of the same trip
                            collec_of_trips.append(collec_num)

                        else:
                            trip_id = trip_id + 1 #assign a new trip id
                            row_ids.append(trip_id)
                            collec_num = 1 #is a new trip, so reset collection number
                            collec_of_trips.append(collec_num)

                    elif next_month.get(prev_trip['Month']) == row['Month']:
                        days_left = days_in_month.get(prev_trip['Month']) - prev_trip['Day'] #number of days left in month
                        #1 because months 1 indexed not zero indexed, if (buffer - days_left) is possitive, the day in the current month
                        #can be included in the trip of the previous month. Otherwise it is negative and range returns an empty list.
                        days_in_new_month = 1 + buffer - days_left
                        #range starts with 1 (first day in the month, add 1 to upper range because it is exclusive
                        day_range = list(range(1, days_in_new_month + 1)) #range of days that are valid to be included in the same trip

                        if row['Day'] in day_range: #is in the same trip
                            row_ids.append(trip_id) #use the same trip id
                            collec_num = collec_num + 1 #increment collection number in the trip because it is part of the same trip
                            collec_of_trips.append(collec_num)

                        else:
                            trip_id = trip_id + 1 #assign a new trip id
                            row_ids.append(trip_id)
                            collec_num = 1 #is a new trip, so reset collection number
                            collec_of_trips.append(collec_num)

                    else:
                        trip_id = trip_id + 1 #assign a new trip id
                        row_ids.append(trip_id)
                        collec_num = 1 #is a new trip, so reset collection number
                        collec_of_trips.append(collec_num)

                else: #if GN and EL trips are not the only ones in the data, each collection is a trip for those data
                    trip_id = trip_id + 1
                    row_ids.append(trip_id)
                    collec_num = 1 #is a new trip, so reset collection number
                    collec_of_trips.append(collec_num)

        fish_sum['TripID'] = row_ids
        fish_sum['CollecNum'] = collec_of_trips
        return fish_sum

    #remove trips that occur accross on a single day and caught less than cutoff number off fish
    def rem_one_collec_gn_trips(self, fish_sum, cutoff):
        """
        Removes gn net trips that only have one collection and caught less than the cutoff of fish.

        Parameters:
            fish_sum (Pandas.DataFrame): The fish dataframe summarized by collections with trip ids. Must have the following columns: 'Year', 'Location', 'Site', 'Gear', 'Month', 'Day', 'TripID', 'Fish Count'.
            cutoff (int): The number of fish caught in a single collection trip that are considerd too few be an actual trip.
        Returns:
            (Dataframe) The trip summary table with error trips removed.
        """
        layers = ['TripID', 'Gear']
        feature = 'Day'
        calcs = ['count']
        titles = ['Day Count']

        #count the number of collections in each trip
        grouped_multiple = fish_sum.groupby(layers).agg({feature: calcs})
        grouped_multiple.columns = titles
        grouped_multiple = grouped_multiple.reset_index()
        trip_day_count = grouped_multiple
        one_day_trips = trip_day_count[trip_day_count['Day Count'] == 1] #trips only with one collection

        #ids on GN one collection trips (EL trips are supposed to be one day)
        gn_one_day = one_day_trips[one_day_trips['Gear'] == 'GN'] #many are likely errors

        gn_one_full_rows = fish_sum[fish_sum['TripID'].isin(gn_one_day['TripID'])]
        gn_error_rows = gn_one_full_rows[gn_one_full_rows['Fish Count'] <= cutoff]

        fish_sum.drop(gn_error_rows.index, inplace=True)
        return fish_sum

    #remove trips that occur accross an entire trip (potentially multiple days) and caught less than cutoff number off fish
    def rem_small_trips(self, fish_sum, gn_cutoff, el_cutoff):
        """
        Removes gn net trips with any number of collections that caught less than the cutoff of fish. Can distiguish between gill-net and electrofishins trips.

        Parameters:
            fish_sum (Pandas.DataFrame): The fish dataframe summarized by collections with trip ids. Must have the following columns: 'Year', 'Location', 'Site', 'Gear', 'Month', 'Day', 'TripID', 'Fish Count'.
            gn_cutoff (int): Fish catch in a gill-net trip equal to or lower are removed from the data.
            el_cutoff (int): Fish catch in a electrofishing trip equal to or lower are removed from the data.
        Returns:
            (Dataframe) The trip summary table with error trips removed.
        """
        layers = ['TripID', 'Gear']
        feature = 'Fish Count'
        calcs = ['sum']
        titles = ['Trip Fish Count']

        grouped_multiple = fish_sum.groupby(layers).agg({feature: calcs})
        grouped_multiple.columns = titles
        grouped_multiple = grouped_multiple.reset_index()

        #ids on GN one day trips (EL trips are supposed to be one day)
        gn_low_count = grouped_multiple[(grouped_multiple['Gear'] == 'GN') & (grouped_multiple['Trip Fish Count'] <= gn_cutoff)]
        gn_error_rows = fish_sum[fish_sum['TripID'].isin(gn_low_count['TripID'])]

        #remove small el trip counts
        el_low_count = grouped_multiple[(grouped_multiple['Gear'] == 'EL') & (grouped_multiple['Trip Fish Count'] <= el_cutoff)]
        el_error_rows = fish_sum[fish_sum['TripID'].isin(el_low_count['TripID'])]

        fish_sum.drop(el_error_rows.index, inplace=True)
        return fish_sum

    def get_trip_summary(self, fish_df, buffer, one_collec_cutoff, trip_gn_cutoff, trip_el_cutoff):
        """
        Creates a table that summarizes what collections happened and what trips they are part of while removing likely erroneous trips.

        Parameters:
            fish_df (Pandas.DataFrame): The fish dataframe to count trips in. Must have the following columns: 'Year', 'Location', 'Site', 'Gear', 'Month', 'Day'.
            buffer (int): The number of days that can occur between collections while still including them in the same trip.
            one_collec_cutoff (int): The number of fish caught in a single collection trip that are considerd too few be an actual trip.
            trip_gn_cutoff (int): Fish catch in a gill-net trip equal to or lower are removed from the data.
            trip_el_cutoff (int): Fish catch in a electrofishing trip equal to or lower are removed from the data.

        Returns:
            (Dataframe) The trip summary table with error trips removed.
        """
        fish_sum = self.collec_fish_count(fish_df)
        trip_sum = self.assign_trip_ids(fish_sum, buffer)
        trip_sum = self.rem_one_collec_gn_trips(trip_sum, one_collec_cutoff)
        trip_sum = self.rem_small_trips(trip_sum, trip_gn_cutoff, trip_el_cutoff)
        return trip_sum

    #'TripID' and 'Fish Count' columns must not be removed from the trip_df

    def cpue_gn_calc(self, fish_df, trip_df, layers, nets = 4, nights = 2):
        """
        Calculates CPUE on any subset of the data that has at least one of the item in ['Year', 'Month', 'Gear', 'Location', 'Site'} and optionally items in ['Species', 'Sex'].

        Parameters:
            fish_df (Pandas.DataFrame): The fish dataframe that has fish you wish to include in CPUE calculations (usually the entire fish dataframe, but filtering is acceptable).
            trip_df (Pandas.DataFrame): A trip summary dataframe that outlines all valid trips.
            layers: The layers to group by and compute CPUE over.
            nets: Number of nets used per trip. Defaults to 4.
            nights: Number of night the nets were left out each trip. Defaults to 2.

        Returns:
            (Dataframe) A table with the CPUE of each group defined with the layers parameter.
        """

        trip_df = trip_df[trip_df['Gear'] == 'GN'] #only care about gill-nets

        #if gear column not filtered out, only include gill-nets
        if 'Gear' in fish_df.columns:
            fish_df =  fish_df[fish_df['Gear'] == 'GN']
        if 'Gear' in trip_df.columns:
            trip_df = trip_df[trip_df['Gear'] == 'GN']

        #****************using trip_df****************
        #----------------------------Fish caught each full trip in each group of the summary table----------------------------
        layers0 = list(set(layers) & set(trip_df.columns)) #intersection of columns to only get layers that fit trips
        layers0.append('TripID')

        feature0 = 'Fish Count'
        calcs0 = ['sum']
        titles0 = ['Fish Count']

        grouped_multiple0 = trip_df.groupby(layers0).agg({feature0: calcs0})
        grouped_multiple0.columns = titles0
        grouped_multiple0 = grouped_multiple0.reset_index()

        #---------------------------------count trips per given period-----------------------------------------------
        layers1 = layers0
        layers1.remove('TripID')
        feature1 = 'TripID'
        calcs1 = ['count']
        titles1 = ['Trip Count']

        grouped_multiple1 = grouped_multiple0.groupby(layers1).agg({feature1: calcs1})
        grouped_multiple1.columns = titles1
        grouped_multiple1 = grouped_multiple1.reset_index()
        fish_count_sum = grouped_multiple1

        #****************using fish_df****************
        #------------------------------number of fish caught for each group------------------------------
        feature2 = layers[-1] #count the smallest group in the data (represents individual trip entries)
        calcs2 = ['count']
        titles2 = ['Fish Count']

        grouped_multiple2 = fish_df.groupby(layers).agg({feature2: calcs2})
        grouped_multiple2.columns = titles2
        grouped_multiple2 = grouped_multiple2.reset_index()

        #****************using summarized fish_df and summarized trip_df****************
        cpue_table = grouped_multiple2.merge(fish_count_sum) #merge the dataframes so only fish entries that match a trip are kept

        #calculate CPUE
        cpue_table['CPUE'] = cpue_table['Fish Count'] / (cpue_table['Trip Count'] * nets * nights)

        return cpue_table
