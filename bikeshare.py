import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    #define ranges of acceppted user input)
    valid_cities = ['chicago','new york city','washington']
    valid_timefilters = ['month','day','both','none']
    valid_months = ['january','february','march','april','may','june','july','august','september','october','november','december','all']
    valid_days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday','all']

    #get user input for city (chicago, new york city, washington)
    city = str(input('Would you like to see data for Chicago, New York City or Washington?\n')).lower()
    while(city not in valid_cities):
        city = str(input('Chosen city not correct.Please choose one of the proposed cities!\n')).lower()

    #get user input for "Would you like to filter for month/day"
    timefilter = str(input('Would you like to filter by month, day, both or not at all?\nIf not at all, please type none. Otherwise, choose month, day or both.\n')).lower()
    while(timefilter not in valid_timefilters):
        timefilter = str(input('Choose a valid entry like month, day, both, none!\n')).lower()

    #get user input for month
    month = ''
    if timefilter in ['month','both']:
        month = str(input('Please choose a month (e.g. January, February, etc...)\n')).lower()
        while(month not in valid_months):
            month = str(input('Pleas choose a valid month (e.g. January, February, etc...)\n')).lower()

    #get user input for day
    day = ''
    if timefilter in ['day','both']:
        day = str(input('Please choose a day (e.g. Monday, Tuesday, etc...)\n')).lower()
        while(day not in valid_days):
            day = str(input('Please choose a valid day (e.g. Monday, Tuesday, etc...)\n')).lower()

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    if city == 'new york city':
        city = 'new_york_city'
    df = pd.read_csv(city + '.csv')

    df['month'] = pd.DatetimeIndex(df['Start Time']).month
    df['month'] = df['month'].astype(str)
    df['day'] = pd.to_datetime(df['Start Time']).dt.dayofweek
    df['day'] = df['day'].astype(str)
    df['hour'] = pd.to_datetime(df['Start Time']).dt.hour

    df['month'] = df['month'].replace(['1','2','3','4','5','6','7','8','9','10','11','12'],['january','february','march','april','may','june','july','august','september','october','november','december'])
    df['day'] = df['day'].replace(['0','1','2','3','4','5','6'],['monday','tuesday','wednesday','thursday','friday','saturday','sunday'])

    df['trip'] = 'from [' + df['Start Station'] + '] to [' + df['End Station'] + ']'

    if month != '' and day == '':
        df = df[df['month'] == month]
    if month == '' and day != '':
        df = df[df['day'] == day]
    if month != '' and day != '':
        df = df[(df['month'] == month) & (df['day'] == day)]

    return df


def show_snapshot(df):
    """
    Shows raw data (each time 5 rows) to the user.

    Args:
        pandas.DataFrame df - name of the dataset which has to be analyzed

    """
    valid_feedback = ['yes','no']
    user_feedback = str(input("Would you like to see some lines of the data set? Please answer. Enter yes or no!\n")).lower()
    while(user_feedback not in valid_feedback):
        user_feedback = str(input("Please enter yes or no!\n")).lower()
    x = 0
    y = 5
    print(df.shape[0])
    while(user_feedback == "yes" and y < df.shape[0]):
        print(df[x:y])
        user_feedback = str(input("Would you like to see some more lines of the data set? Please answer. Enter yes or no!\n")).lower()
        x += 5
        y += 5

def time_stats(df,city,month,day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    #displaying the most common month only makes sense when months are not filtered
    if month == '':
        print('The most common month for sharing a bike is {}'.format(df['month'].mode()[0]))
    #displaying the most common weekday only makes sense when weekdays are not filterd
    if day == '':
        print('The most common day of week for sharing a bike is {}'.format(df['day'].mode()[0]))
    print('The most common start hour for sharing a bike is {}'.format(df['hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #displaying most commonly used start station
    print('The most commonly used start station is {}'.format(df['Start Station'].mode()[0]))
    print('The most commonly used end station is {}'.format(df['End Station'].mode()[0]))
    print('The most frequent trip is {}'.format(df['trip'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #displaying the total travel time in hours
    print('The total travel time is approximately {} hours'.format(df['Trip Duration'].sum() // 3600))

    #displaying mean travel time in seconds (rounded to 0 decimals)
    print('The mean travel time is approximately {} seconds'.format(df['Trip Duration'].mean().round(decimals = 0)))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()


    #displaying counts of user types
    print('The data set shows the following distribution regarding User Type.')
    print(df['User Type'].value_counts())

    #gender and birth year only relevant for New York City and Chicago
    if city in ['new york city','chicago']:
    #displaying counts of gender
        print('\nFollowing information could give you some insight into data quality of the column gender.')
        print('{} percent of the rows do not contain a value for gender'.format(int(sum(df['Gender'].isnull()) / df.shape[0] * 100)))
        print('Rows containing gender information show the following distribution.')
        print(df['Gender'].value_counts())

    #displaying earliest, most recent, and most common year of birth
        print('\nFollowing information could give you some insight into data quality of the column birth year.')
        print('{} percent of the rows do not contain a value for birth year'.format(int(sum(df['Birth Year'].isnull()) / df.shape[0] * 100)))
        print('In order to determine the correct mode, nans will be dropped')
        df = df.dropna(subset=['Birth Year'])
        df['Birth Year'] = df['Birth Year'].astype(str).str.slice(0,4)
        print('The most common year of birth is {}'.format(df['Birth Year'].mode()[0]))
        print('The earliest year of birth is {}'.format(df['Birth Year'].min()))
        print('This implicates that the oldest customer is {} year(s) old.'.format(2017 - int(df['Birth Year'].min())))
        print('The latest year of birth is {}'.format(df['Birth Year'].max()))
        print('This implicates that the youngest customer is {} year(s) old.'.format(2017 - int(df['Birth Year'].max())))
        print('Taking into account the ratio of filled rows, the age of the oldest and youngest customers: Please ask yourself how much you can trust the data quality of birth year :-)')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        if not df.empty:
            show_snapshot(df)
            time_stats(df,city,month,day)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df,city)
        else:
            print("No data available for your selection. Please try another filter!")
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
