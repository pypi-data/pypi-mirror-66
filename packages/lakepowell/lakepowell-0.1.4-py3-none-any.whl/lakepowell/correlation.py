import lakepowell
import pandas as pd
import numpy as np
from scipy.stats.stats import pearsonr


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
