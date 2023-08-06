# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 13:19:05 2020

@author: aquag
"""
#maybe make a variable.
#availiabel variables 
#time frame
    #year
    #month
    #trip?
#biotic factor

def calc_catch_per_unit_effort(data,time, bio_fac):
    #pull weights
   

    #or this should be length?


    #divide by hours = 32?? overnight???
    #get average number of hours
    
    #divide by number of nets = number of sites = 32??
    #do this by taking the site column
    #pull out and coutn unique values
    
    #also get avearge net size
    #have this as a sencondary caracterstic based on what gets imported

    #time period
    # so sort out the data based on what they send
    if time == 'year':
        pass
    elif time == 'month':
        pass
    elif time == 'trip':
        pass
    else:
        #incorect variable, spit out error
        pass


    #add up variable(fish, length, weight)
    if bio_fac == 'fish':
        #add up number of fish
        calac_varaible = len(data)
        pass
    elif bio_fac == 'length':
        length = data['Length']
        calac_varaible = sum(length)
        pass
    elif bio_fac == 'weight':
         weights = data["Weight"]
        #add together
        calac_varaible = sum(weights)
    else:
        #error, return error message?
        pass
    #then pull the variable they want
    #divide by number of sites in colection
    sites = data['Site']
    total_sites = len(set(sites))
    Catch_per = calac_varaible / total_sites
    
    return Catch_per