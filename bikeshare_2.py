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
    print('Hello! Let\'s explore some US bikeshare data!\n')

    #Get user input for city (chicago, new york city, washington).
    city = input("Which city would you like to see the data: Chicago, New York or Washington? \n").lower()
    #Data Validation for City
    while city not in ("chicago","new york","washington"):
        print("\nPlease, select a valid city!")
        city = input("\nSelect one of the following cities: Chicago, New York or Washington? \n").lower()

    print("The chosen city was {}\n".format(city.title()))

    #Get user input for month (all, january, february, ... , june)
    month = input("Which month do you want to filter? January, February, March, April, May, June, or 'all'?\n").lower()
    #Data Validation for month
    while month not in ("january","february","march","april","may","june","all"):
        print("\nPlease, select a valid month!")
        month = input("`nWhich month do you want to filter? January, February, March, April, May, June, or 'all'?\n").lower()

    print("The chosen month was {}\n".format(month.title()))

    #Get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Which day would you like to take a look? Sunday, Monday, Tuesday, or 'all'?\n").lower()
    #Data validation for weekday
    while day not in ("sunday","monday","tuesday","wednesday","thursday","friday","saturday","all"):
        print("\nPlease, select a valid day!")
        day = input("\nWhich day would you like to take a look? Sunday, Monday, Tuesday, or 'all'?\n").lower()

    print("The chosen day was {}\n".format(day.title()))

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

    #load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    #convert the Start Time Column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month ]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def raw_data_viz(df):
    """Show some raw data for the user if they want to"""

    question = input("\nEnter yes if you would you like to see all availabe columns and 5 rows of data. Enter 'no' to go direct to statistics.\n").lower()
    x = 0
    while question != "no":
        print(df.iloc[x:x+5, : ])
        x = x + 5
        question = input("\nWould you like to see the next 5 data rows?\n").lower()


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #Display the most common month
    popular_month = df['month'].mode()[0]
    print("\nThe most popular month was {}".format(popular_month))

    #Display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print("\nThe most popular week day was {}".format(popular_day))

    #Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("\nThe most popular hour was {}".format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #Display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print("\nThe most popular Start Station was {}".format(popular_start_station))

    #Display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print("\nThe most popular End Station was {}".format(popular_end_station))

    #Display most frequent combination of start station and end station trip
    #Concatenate Start and End Station to create a unique value
    df['Combination'] = df['Start Station'].str.cat(df['End Station'],sep=" - ")

    #mode of this unique value
    most_common_combination = df['Combination'].mode()[0]

    #split again to get their parts
    combination_split = most_common_combination.split(" - ")
    print("\n Thes most common frequent combination of station on the period is: Start Station, {} and End Station, {}  ".format(combination_split[0],combination_split[1]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #Display total travel time
    total_trip_duration = df['Trip Duration'].sum(axis=0)
    print("\nThe total trip duration of the selected period was {} min".format(total_trip_duration/60))

    #Display mean travel time
    mean_trip_duration = df['Trip Duration'].mean(axis=0)
    print("\nThe mean trip duration of the selected period was {} min".format(mean_trip_duration/60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #Display counts of user types
    user_types = df['User Type'].value_counts()
    print(user_types)
    print("\n")

    #Display counts of gender
    try:
        user_gender = df['Gender'].value_counts()
        print(user_gender)
    except:
        print("\nWe've tried to show the users gender, but the selected city doesn't have this data on the database.")

    #Display earliest, most recent, and most common year of birth
    try:
        earliest_date = df['Birth Year'].min()
        print("\nThe oldest user was born in {}".format(earliest_date))
    except:
        print("\nWe've tried to show some age statistics of users, but the selected city doesn't have the birth year on the database.")

    try:
        most_recent_date = df['Birth Year'].max()
        print("\nThe youngest user was born in {}".format(most_recent_date))
    except:
        print("\nWe've tried to show some age statistics of users, but the selected city doesn't have the birth year on the database.")

    try:
        most_common_year = df['Birth Year'].mode()[0]
        print("\nThe most common birth year is {}".format(most_common_year))
    except:
        print("\nWe've tried to show some age statistics of users, but the selected city doesn't have the birth year on the database.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        raw_data_viz(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
