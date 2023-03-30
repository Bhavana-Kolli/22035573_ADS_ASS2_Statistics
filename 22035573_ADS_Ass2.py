#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
7PAM2000 Applied Data Science 1
Assignment 2: Statistics and trends

@author: Bhavana Kolli - 22035573
"""

# Here modules are imported

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import stats

# Here functions for all plots are defined

def read_df(filename):
    """
    Reads a dataframe in World Bank format from a CSV file.
    Returns two dataframes: one with years and other as countries as columns. 
    The function cleans theransposed dataframe by dropping unnecessary columns
    and rows with missing data.
    Args:
        filename (str): the name of the CSV file to be read
    Returns:
        df_countries(pd.DataFrame): 
            a dataframe with years as rows and countries as columns
        df_years(pd.DataFrame): 
            a dataframe with countries as rows and years as columns
    """
    
    # read the CSV file
    df = pd.read_csv(filename, skiprows=4)
    
    # drops unnecessary columns
    df.drop(['Country Code', 'Indicator Name', 'Indicator Code'], axis=1, 
            inplace=True)
    
    # sets the index to the country name
    df = df.set_index('Country Name')
    
    # drops rows and columns with all missing data
    df.dropna(axis=0, how='all', inplace=True)
    df.dropna(axis=1, how='all', inplace=True)
    
    # transpose the dataframe
    df_t = df.transpose()
    
    # convert the index to years
    df_t.index = pd.to_datetime(df_t.index, format='%Y').year
    
    # sets column and index names
    df_t.columns.name = 'Country Name'
    df_t.index.name = 'Year'
    
    # a dataframe countries as columns
    df_countries = df_t
    
    # a dataframe with years as columns
    df_years = df_countries.T
    
    return df_countries, df_years 


df_c, df_y = read_df("access to electricity.csv")
