import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
            'new york city': 'new_york_city.csv',
            'washington': 'washington.csv'}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # While loop to validate and return the user input ensuring the correct city name was entered to break
    while True:
        city = input(
                    "Please choose one of these cities to explore: Chicago, New York City, or Washington:\n"
                    ).lower()
        if city not in CITY_DATA:
            print("\nCity not found!")
            continue  
        else:
            print(
                f"\nYou have chosen to explore {city.title()}."
                )
            break
    # While loops validating user input for filtering by month and day. Each loop validate month and day inputs, invalid inputs will restart the loop.
    while True:
        month = input(
                     "Please choose a month from:\nJanuary, Feburary, March, April, May, June, or type 'all' to explore all monthly data\n"
                     ).lower()
        month_list = ["january", "february", "march", "april", "may", "june", "all"]
        if month != 'all' and month not in month_list:
            print("\nInvalid Input!\n")
            continue
        else:
            print(
                 f"\nYou have chosen to explore {month.title()} from monthly data."
                 )
            break
         
    while True:
        day = input(
                   "Please choose a weekday, or type 'all' to explore all daily data\n"
                   ).lower()
        days_list = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday", "all"]
        if day != 'all' and day not in days_list:
            print("\nInvalid Input!\n")
            continue
        else:
            print(f"\nYou have chosen {day.title()} to explore daily data.")
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
    print("Data is being prepared!")

    df = pd.read_csv(CITY_DATA[city])
    # Converting [Start Time] column to DateTime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # Creating [Month] and [Day] columns from [Start Time] column data.
    df['Start_Month'] = df['Start Time'].dt.month
    df['Start_Day'] = df['Start Time'].dt.day_name()
    # Validating month filter if specified 
    if month != 'all':
        # Use index of month +1 to get the correct month number
        months = ["january", "february", "march", "april", "may", "june"]
        month = months.index(month) + 1
        # Create a new df filtered by month
        df = df[df['Start_Month'] == month]
    # Validating day filter if specified    
    if day != 'all':
        # Create a new df filtered by day
        df = df[df['Start_Day'] == day.title()]
    
    print('-'*40)
    return df

        
def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Returning the most common/popular month.
    common_month = df['Start_Month'].mode()[0]
    print(f"Most popular month is: {common_month}")

    # Returning the most common/popular day.
    common_day = df['Start_Day'].mode()[0]
    print(f"Most popular day is: {common_day}")
    
    # Returning the most common/popular starting hour based on user input.
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print(f"Most popular hour is: {popular_hour}:00 HRS")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Aggregatin the most common/popular starting station from [Start Station] column.
    most_popular_start_station = df['Start Station'].mode()[0]
    print(f"Most popular starting station is: {most_popular_start_station}")
    
    # Aggregatin the most common/popular ending station from [End Station] column.
    most_popular_end_station = df['End Station'].mode()[0]
    print(f"Most popular End station is: {most_popular_end_station}")
    
    # Display most frequent combination of start station and end station by combining them and extracting the mode of the new df.
    df['combination'] = df['Start Station'] + ' AND ' + df['End Station']
    most_frequent_start_and_end_stations = df['combination'].mode()[0]
    print(
         f"Most frequent start station and end stations are: {most_frequent_start_and_end_stations}"
         )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Calculating the total travel time from [Trip Duration] column
    total_travel_time = df['Trip Duration'].sum()
    print(f"Total travel time in secounds is: {total_travel_time}, \
    and in hours: {total_travel_time/3600}")

    # Calculating the average travel time
    average_travel_time = df['Trip Duration'].mean()
    print(f"Average travel time in secounds is: {average_travel_time}, \
        and in hours: {average_travel_time/3600}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Extracting the counts of user types from [User Type] column
    print("User Types are:\n", df['User Type'].value_counts())

    # Extracting gender count from [Gender] column
    if 'Gender' in df:
        print(f"User genders count are:\n", df['Gender'].value_counts())

    # Extracting earliest, most recent, and most common year of birth conditioned if [Birth Year] column available
    if 'Birth Year' in df:
            earliest_birth_year = int(df['Birth Year'].min())
            print(f"Earliest birth year is: {earliest_birth_year}")

            recent_birth_year = int(df['Birth Year'].max())
            print(f"Most recent birth year is: {recent_birth_year}")

            common_birth_year = int(df['Birth Year'].mode()[0])
            print(f"Most common birth year is: {common_birth_year}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def show_raw_data(df):
    """Return sudsequent rows from DataFrame based of user answer
    Args:
    df - Pandas DataFrame containing city data filtered by month and day from load_data()
    """
    display_rows = 0
    answer = input("Would you like to view first 5 rows of data? [Yes/No]:\n").lower()
    # Validating user input using while loop
    while True:
        if answer == 'no':
            break
        print(df[display_rows:display_rows + 5])
        answer = input("Would you like to view next 5 rows of data? [Yes/No]:\n").lower()
        display_rows += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart != 'yes':
            break


if __name__ == "__main__":
	main()