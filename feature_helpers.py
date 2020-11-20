# USEAGE
# Each function takes 'df' as pandas dataframe object and returns the modified dataframe.
# add_locs also takes a datafrane of the locations
# example:
#   data = pd.read_csv("weatherAUS.csv")
#   data = wind_vectors(data)
#   locations = pd.read_csv("lcoations.csv")
#   data = add_locs(data, locations)

import pandas as pd
import numpy as np
import datetime

# add location coordinates
def add_locs(df, location_df):
    return df.join(location_df.set_index('Location'), on='Location')

# convert yes and no strings to binary
def binary_target(df):
    df = df["RainTomorrow"].replace(('Yes', 'No'), (1, 0))
    df = df["RainToday"].replace(('Yes', 'No'), (1, 0))
    return df

def wind_vectors(df):
    df = df['WindGustDir'].replace(
        ('N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW','SW','WSW','W','WNW','NW','NNW'),
        (0, 22.5, 45, 67.5, 90, 112.5, 135, 157.5, 180, 202.5, 225, 247.5, 270, 292.5, 315, 337.5)
    )

    df = df['WindDir9am'].replace(
        ('N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW','SW','WSW','W','WNW','NW','NNW'),
        (0, 22.5, 45, 67.5, 90, 112.5, 135, 157.5, 180, 202.5, 225, 247.5, 270, 292.5, 315, 337.5)
    )

    df = df['WindDir3pm'].replace(
        ('N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW','SW','WSW','W','WNW','NW','NNW'),
        (0, 22.5, 45, 67.5, 90, 112.5, 135, 157.5, 180, 202.5, 225, 247.5, 270, 292.5, 315, 337.5)
    )

    wv = df.pop('WindGustSpeed')
    wd = df.pop('WindGustDir')*np.pi/180
    df['WindGustX'] = wv*np.cos(wd)
    df['WindGustY'] = wv*np.sin(wd)

    wv = df.pop('WindSpeed9am')
    wd = df.pop('WindDir9am')*np.pi/180
    df['Wind9amX'] = wv*np.cos(wd)
    df['Wind9amY'] = wv*np.sin(wd)

    wv = df.pop('WindSpeed3pm')
    wd = df.pop('WindDir3pm')*np.pi/180
    df['Wind3pmX'] = wv*np.cos(wd)
    df['Wind3pmY'] = wv*np.sin(wd)

    return df

def date_to_signal(df):
    data_date = pd.to_datetime(df.pop('Date'))
    timestamp_s = data_date.map(datetime.datetime.timestamp)
    day = 24*60*60
    year = (365.2425)*day
    df['daysin'] = np.sin(timestamp_s * (2 * np.pi/day))
    df['daycos'] = np.cos(timestamp_s * (2 * np.pi/day))
    df['yearsin'] = np.sin(timestamp_s * (2 * np.pi/year))
    df['yearcos'] = np.cos(timestamp_s * (2 * np.pi/year))

    return df


def all_augments(df, location_df):
    df = add_locs(df, location_df)
    df = wind_vectors(df)
    df = date_to_signal(df)