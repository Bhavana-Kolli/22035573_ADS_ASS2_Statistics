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
    plt.savefig('456.png', dpi=300)
    plt.show()


def plot_distribution(df_emissions, df_electricity, countries):
    """
    Plots the distribution of access to electricity and CO2 emissions 
    across all years for the selected countries
    Parameters:
    df_emissions (pandas.DataFrame): contains CO2 emissions data
    df_electricity (pandas.DataFrame): contains access to electricity data
    countries (list): list of country names to be included in the plot

    Returns:
    None
    """
    # years with 5 year increment from 1990 to 2019
    years = [1990, 1995, 2000, 2005, 2010, 2015, 2019]
    # subplot
    fig, axs = plt.subplots(1, 2, figsize=(12, 4))
    # CO2 emissions distributions over time for a few countries
    df_emissions_c.loc[years, countries].plot.bar(ax=axs[0], xlabel='Years', 
                                              ylabel='CO2 Emissions')
    axs[0].legend(bbox_to_anchor=(1, 1), loc='upper left')
    # access to electricity over time for a few countries
    df_electricity_c.loc[years, countries].plot.bar(ax=axs[1], xlabel='Years', 
                                                ylabel='Access to Electricity')
    axs[1].legend(bbox_to_anchor=(1, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('123.png', dpi=300)
    plt.show()


def plot_skew_kurt(df, title):
    """
    Plot skewness and kurtosis for a given DataFrame.

    Parameters:
        df(pandas.DataFrame): The DataFrame to calculate skewness and kurtosis
        title (str): The title to use for the plot.

    """
    # Calculate skewness and kurtosis for each column
    skewness = pd.DataFrame({'Skewness': stats.skew(df)})
    kurtosis = pd.DataFrame({'Kurtosis': stats.kurtosis(df)})
    sk_df = skewness.join(kurtosis)

    # Plot the results
    fig, axs = plt.subplots(1, 2, figsize=(12, 4))
    
    # Plot the skewness chart
    sk_df['Skewness'].plot(kind='bar', ax=axs[0], 
                           title=title + ' Skewness')
    
    # Plot the kurtosis chart
    sk_df['Kurtosis'].plot(kind='bar', ax=axs[1], 
                           title=title + ' Kurtosis')
    
    # Add labels to the y axes
    axs[0].set_ylabel('Skewness')
    axs[1].set_ylabel('Kurtosis')
    
    # Add spacing between the plots
    plt.tight_layout()
    
    # Display the plot
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


# Plot-1 (Time Series) ----------------------------------------------------


# Trend of CO2 emissions and access to electricity over time forfew countries.
plot_elect_and_emiss(df_electricity_c, df_emissions_c, countries)



# Plot-2 (line chart) ----------------------------------------------------

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

# plot line chart of correlation coefficient over time
plt.plot(corr_time.index, corr_time)
plt.xlabel('Year')
plt.ylabel('Correlation coefficient')
plt.title('Correlation between electricity access and CO2 emissions over time')
plt.show()


# Plot-3 (Stacked Bar) --------------------------------------------------

# calculate mean access to electricity for the year 2019 
df_electricity_y_mean = df_electricity_y.groupby('Country Name')[2019].mean()
# calculate mean CO2 emissions for the year 2019 
df_emissions_y_mean = df_emissions_y.groupby('Country Name')[2019].mean()


# bar chart for mean access to electricity and mean CO2 emissions 
# for the year 2019 for all selected countries
fig, ax = plt.subplots(figsize=(8, 6))

ax.bar(df_electricity_y_mean[countries].index, 
       df_electricity_y_mean[countries].values, label='Access to Electricity')
ax.bar(df_emissions_y_mean[countries].index, 
       df_emissions_y_mean[countries].values, label='CO2 Emissions')

ax.set_xlabel('Country')
ax.set_ylabel('Mean Value')
ax.set_title('Mean of Access to Electricity and Mean CO2 Emissions for 2019')
ax.legend()

plt.show()


# Plot-4 (Distribution) ----------------------------------------------------


# bar chart distribution of access to electricity and CO2 emissions
# across all years for the selected countries
plot_distribution(df_emissions_c, df_electricity_c, countries)


# Plot-5 (skewness and kurtosis)--------------------------------------------


# skewness and kurtosis of Access to electricity for selected countries
plot_skew_kurt(df_electricity_c[countries], 'Access to electricity')
# skewness and kurtosis of CO2 emissions for selected countries
plot_skew_kurt(df_emissions_c[countries], 'CO2 emissions')

