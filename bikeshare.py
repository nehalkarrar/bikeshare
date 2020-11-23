import time
import pandas as pd
import numpy as np
import calendar

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
    cities = ['chicago', 'new york city', 'washington']
    city = input("Would you like to see the data for chicago, new york city or washington?\n").lower()
    while True:
        if (city not in cities):
            city = input("Would you like to see the data for chicago, new york city or washington?\n")
        else:
            break

    # get user input for month (all, january, february, ... , june)
    months = ['all', 'january', 'february', 'march', 'april', 'may' , 'june']
    month = input("Which month? all, january, february, march, april, may , june \n").lower()
    while True:
        if (month not in months):
            month = input("Which month? all, january, february, march, april, may , june \n")
        else:
            break


    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['all','0','1','2','3','4','5','6']
    day = input("Which day? please type your response as an integer (e.g., 1 = Sunday) \n").lower()
    while True:
        if (day not in days):
            day = input("Which day? please type your response as an integer (e.g., 1 = Sunday) \n")
        else:
            break


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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df["Start Time"])

    # extract month and day of week from Start Time to create new columns
    df['month'] = pd.to_datetime(df['Start Time'], format='%H:%M:%S').dt.month
    df['day_of_week'] = pd.to_datetime(df['Start Time'], format='%H:%M:%S').dt.dayofweek
    df['day_name'] = pd.to_datetime(df['Start Time'], format='%H:%M:%S').dt.day_name()


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
        df = df[df['day_of_week'] == int(day)]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].value_counts().idxmax()
    print('Most popular month:', popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].value_counts().idxmax()
    day_name = list(calendar.day_name)
    print('Most popular day:', popular_day, ' - ',day_name[popular_day] )

    # display the most common start hour
    df['hour'] = pd.to_datetime(df['Start Time'], format='%H:%M:%S').dt.hour
    popular_hour = df['hour'].value_counts().idxmax()
    print('Most popular Hour:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].value_counts().idxmax()
    print('Most popular start station:', popular_start_station)

    # display most commonly used end station
    popular_end_station = df['End Station'].value_counts().idxmax()
    print('Most popular end station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    popular_combination_station = (df['Start Station'] + ';' + df['End Station']).mode()
    print('Most popular end station:', popular_combination_station)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    #travel_time = pd.to_datetime(df['End Time']) - pd.to_datetime(df['Start Time'])
    Total_travel_time = np.sum(df['Trip Duration'])
    print("Total travel Time: ", Total_travel_time)

    # display mean travel time
    Avg_travel_time = df['Trip Duration'].mean()
    print("Average travel Time: ", Avg_travel_time)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("User types: \n", user_types)

    # Display counts of gender
    if('Gender' in df.columns):
        count_genders = df['Gender'].value_counts()
        print("Counts of users genders: \n", count_genders)
    else:
        print(" Gender information is not available for Washington City")
    

    # Display earliest, most recent, and most common year of birth
    if('Birth Year' in df.columns):
        earliest = df['Birth Year'].min()
        print("Earliest year of birth: \n", int(earliest))

        most_recent = df['Birth Year'].max()
        print("Most recent year of birth: \n", int(most_recent))

        most_common_birth_year = df['Birth Year'].value_counts().idxmax()
        print('Most common year of birth:', int(most_common_birth_year))


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
        display = input('\nWould you like to display raw? Enter yes or no.\n')
        i = 0
        while(display.lower() == 'yes' and i<len(df)):
            print(df.iloc[i:i+5])
            display = input('\nWould you like to display raw? Enter yes or no.\n')
            i += 5


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
