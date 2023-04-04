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


def plot_elect_and_emiss(df_electricity, df_emissions, country_list):
    """
    Plots the access to electricity and CO2 emissions for a list of countries 
    over time in a 2x2 subplot.

    Args:
        df_electricity (pd.DataFrame): A DataFrame containing the percentage 
        of population with access to electricity for different countries 
        and years.
        df_emissions (pd.DataFrame): A DataFrame containing the CO2 emissions 
        per capita for different countries and years.
        
        country_list (list): A list of countries to plot.

    """
    
    # Create a 2x2 subplot and flatten it to iterate over it.
    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    axs = axs.flat
    
    # Iterate over the list of countries to plot.
    for country in country_list:
        
        # Get the next axis in the flattened subplot.
        ax = next(axs)
        
        # Plot the access to electricity on the left axis.
        df_electricity[country].plot(ax=ax, label='Electricity Access')
        
        # Create a twin axis on the right and plot the CO2 emissions.
        ax2 = ax.twinx()
        df_emissions[country].plot(ax=ax2, label='CO2 Emissions', color='red')
        
        # Set labels and titles.
        ax.set_xlabel('Year')
        ax.set_ylabel('Percentage of population')
        ax2.set_ylabel('Metric tons per capita')
        ax.set_title(f'Electricity access and CO2 emissions over time in {country}')
        
        # Add legends to each axis.
        ax.legend(loc='upper left')
        ax2.legend(loc='upper right')

    # Adjust the spacing and show the plot
    plt.tight_layout()
    plt.show()


# Main Program


# Reading Files-------------------------------------------------------


# read the data for "Access to electricity (% of population)" 
df_electricity_c, df_electricity_y = read_df("access to electricity.csv")

# read the data for "CO2 emissions (metric tons per capita)"
df_emissions_c, df_emissions_y = read_df("co2 emissions.csv")


# Summary Statistics--------------------------------------------------


#summary statistics for "Access to electricity(% of population)"of whole world
print("\nAccess to electricity summary statistics for whole world:")
print(df_electricity_c.describe())
print("\nAccess to electricity summary statistics from 1990 to 2019:")
print(df_electricity_y.describe())

#summary statistics for "CO2 emissions(metric tons per capita)"of whole world
print("\nCO2 emissions summary statistics for whole world:")
print(df_emissions_c.describe())
print("\nCO2 emissions summary statistics from 1990 to 2019:")
print(df_emissions_y.describe())

# select a few countries to compare statistical properties
countries = ['United States', 'India', 'China', 'Brazil']

# calculate mean, median, and standard deviation for each country

# "Access to electricity(% of population)" for a few countries
elect_stats = pd.DataFrame({'Mean': df_electricity_c[countries].mean(), 
                            'Median': df_electricity_c[countries].median(), 
                            'Std Dv': df_electricity_c[countries].std()})

# "CO2 emissions(metric tons per capita)" for a few countries
emiss_stats = pd.DataFrame({'Mean': df_emissions_c[countries].mean(), 
                            'Median': df_emissions_c[countries].median(), 
                            'Std Dev': df_emissions_c[countries].std()})

# print the results 
print("\nAccess to electricity statistics for a few countries:")
print(elect_stats)

print("\nCO2 emissions statistics for a few countries:")
print(emiss_stats)


# Correlations--------------------------------------------------


# calculate correlation coefficients between "Access to electricity"
# and "CO2 emissions" over time
corr_time = df_electricity_y.corrwith(df_emissions_y)
print("\nCorrelation between electricity access and CO2 emissions over time:")
print(corr_time)

# calculate correlation coefficients between "Access to electricity"
# and "CO2 emissions" for all countries
corr_countries = df_electricity_c.corrwith(df_emissions_c)
print("\nCorrelation between electricity access and CO2 emissions for world:")
print(corr_countries)


# Plot-1 (Time Series) ------------------------------------------------


# Trend of CO2 emissions and access to electricity over time forfew countries.
plot_elect_and_emiss(df_electricity_c, df_emissions_c, countries)

