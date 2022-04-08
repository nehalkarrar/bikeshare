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
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Please choose a city from Chicago, New York City, Washington: ').lower()
    #cities = ['chicago','new york city', 'washington']
    while True:
        if city in CITY_DATA:
            break
        else:
            input('Invalid city, please enter a city from Chicago, New York City, Washington: ').lower()

    # get user input for month (all, january, february, ... , june)
    month = input('Please enter a month from January to June, or type "all" to display all months: ').lower()
    months = ['all', 'january', 'february', 'march' ,'april','may', 'june']
    while True:
        if month in months:
            break
        else:
            input('Invalid month, please enter a month from January to June, or type "all": ').lower()


    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Please enter a day of the week, or type "all" to display all days: ').lower()
    days = ['all', 'saturday','sunday','monday','tuesday','wedenday','thursday','friday']
    while True:
        if day in days:
            break
        else:
            input('Invalid day, please enter a day of the week, or type "all": ').lower()


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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df["Start Time"])

    # extract month and day of week from Start Time to create new columns
    df['month'] = pd.to_datetime(df['Start Time'], format='%H:%M:%S').dt.month
    df['day_of_week'] = pd.to_datetime(df['Start Time'], format='%H:%M:%S').dt.day_name()


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].value_counts().idxmax()
    print('The most common month is ', common_month)


    # display the most common day of week
    common_dow = df['day_of_week'].value_counts().idxmax()
    print('The most common day of the week is ', common_dow)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    common_hour = df['hour'].value_counts().idxmax()
    print('The most common start hour is ', common_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].value_counts().idxmax()
    print('The most common start station is ', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].value_counts().idxmax()
    print('The most common end station is ', common_end_station)

    # display most frequent combination of start station and end station trip
    common_combination = df.groupby(['Start Station','End Station']).size().idxmax()
    print('The most common start - end station combination is ', common_combination)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    
    total_travel_time = df['Trip Duration'].sum()
    print('Total Travel Time is ', total_travel_time, ' seconds')

    # display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    print('Average Travel Time is ', avg_travel_time, ' seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        genders = df['Gender'].value_counts()
        print(genders)

    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        earliset = df['Birth Year'].min()
        recent = df['Birth Year'].max()
        common_birth = df['Birth Year'].mode()[0]
        print('The earliset birth year ', earliset, ' and the most recent one is ', recent, ' and the most common one is ', common_birth)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
