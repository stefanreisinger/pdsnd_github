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
    print('\nUdacity Project - Bikeshare Analysis')
    print('V1.0 - 18.08.2021 - Stefan Reisinger')
    print('------------------------------------\n')

    print('This program lets you analyze real bikeshare data from the cities Wahsington DC,')
    print('Chicago and New York City in the timespan from January 2017 to June 2017.\n')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('Please choose one of the following cities by entering the city name or the corresponding number:')
    print('    1 - Chicago')
    print('    2 - New York City')
    print('    3 - Washington\n')

    while True:
        city = input('Your choice: ')
        
        if city.isdigit() == True and int(city) in [1, 2, 3]:
            city = list(CITY_DATA.keys())[int(city)-1]
            break
        elif city.lower() in CITY_DATA.keys():
            city = city.lower()
            break
        else:
            print('---> Invalid Input! Please try again!')
            
    # get user input for month (all, january, february, ... , june)
    print('\nPlease choose the month for which the analysis shall be performed by entering the month name')
    print('or the corresponding number. ALL means, that the data is not filtered regarding month.')
    print('    0 - All')
    print('    1 - January')
    print('    2 - February')
    print('    3 - March')
    print('    4 - April')
    print('    5 - May')
    print('    6 - June\n')

    months = ['all','january','february','march','april','may','june']

    while True:
        month = input('Your choice: ')
        
        if month.isdigit() == True and int(month) in range(7):
            month = months[int(month)]
            break
        elif month.lower() in months:
            month = month.lower()
            break
        else:
            print('---> Invalid Input! Please try again!')


    # get user input for day of week (all, monday, tuesday, ... sunday)
    print('\nPlease choose the day of week for which the analysis shall be performed by entering the day name')
    print('or the corresponding number. ALL means, that the data is not filtered regarding day of week.')
    print('    0 - All')
    print('    1 - Monday')
    print('    2 - Tuesday')
    print('    3 - Wednesday')
    print('    4 - Thursday')
    print('    5 - Friday')
    print('    6 - Saturday')
    print('    7 - Sunday\n')

    days = ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']

    while True:
        day = input('Your choice: ')
        
        if day.isdigit() == True and int(day) in range(8):
            day = days[int(day)]
            break
        elif day.lower() in days:
            day = day.lower()
            break
        else:
            print('---> Invalid Input! Please try again!')

    print('\n--> You wish to analyze the bikeshare data for {}'.format(city.title()))
    print('    Filtered by month {} and day of week {}.\n'.format(month.title(), day.title()))

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

    filename = CITY_DATA[city]

    print('--> Loading data from file {} and filtering ...'.format(filename))
    start_time = time.time()

   # load data file into a dataframe
    df = pd.read_csv(filename)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    if month != 'all':
        # filter by month to create the new dataframe
        df = df[df['Start Time'].dt.month_name() == month.title()]

    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Start Time'].dt.weekday_name == day.title()]

    print("    Number of datasets after filtering: {}".format(df.index.size))    
    print("This took %.3f seconds.\n" % (time.time() - start_time))

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('--> Calculating The Most Frequent Times of Travel ...')
    start_time = time.time()

    # display the most common month
    df_month = pd.to_datetime(df['Start Time']).dt.month_name()
    mc_month = df_month.mode().values[0]
    print('    The most common month in the dataset is:         {}'.format(mc_month))
    if month != 'all':
        print('    --> which is no surprise, since you wanted the data filtered by that day')
        
    # display the most common day of week
    df_day = pd.to_datetime(df['Start Time']).dt.weekday_name
    mc_day = df_day.mode().values[0]
    print('    The most common day of week in the dataset is:   {}'.format(mc_day))
    
    # display the most common start hour
    df_hour = pd.to_datetime(df['Start Time']).dt.hour
    mc_hour = df_hour.mode().values[0]
    print('    The most common start hour in the dataset is:    {}'.format(mc_hour))

    print("This took %.3f seconds.\n" % (time.time() - start_time))


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('--> Calculating The Most Popular Stations and Trip ...')
    start_time = time.time()

    # display most commonly used start station
    mc_start_station = df['Start Station'].mode().values[0]
    print('    The most common start station in the dataset is: {}'.format(mc_start_station))

    # display most commonly used end station
    mc_end_station = df['End Station'].mode().values[0]
    print('    The most common end station in the dataset is:   {}'.format(mc_end_station))

    # display most frequent combination of start station and end station trip
    df_trip = df['Start Station'] + ' ---> ' + df['End Station']
    mc_trip = df_trip.mode().values[0]
    print('    The most common trip in the dataset is:          {}'.format(mc_trip))

    print("This took %.3f seconds.\n" % (time.time() - start_time))


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('--> Calculating Trip Duration ...')
    start_time = time.time()

    # display total travel time
    sum_duration = df['Trip Duration'].sum()
    print('    The sum of all trip durations in the dataset is: {} seconds'.format(sum_duration))

    # display mean travel time
    avg_duration = df['Trip Duration'].mean()
    print('    The avg of all trip durations in the dataset is: %.1f seconds' % avg_duration)

    print("This took %.3f seconds.\n" % (time.time() - start_time))


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('--> Calculating User Stats ...')
    start_time = time.time()

    # Display counts of user types
    num_subscribers = df[df['User Type'] == 'Subscriber'].index.size
    print('    The number of Subscribers in the dataset is:     {}'.format(num_subscribers))
    num_customers = df[df['User Type'] == 'Customer'].index.size
    print('    The number of Customers in the dataset is:       {}\n'.format(num_customers))

    if 'Gender' in df:
        # Display counts of gender
        num_male = df[df['Gender'] == 'Male'].index.size
        print('    The number of Males in the dataset is:           {}'.format(num_male))
        num_female = df[df['Gender'] == 'Female'].index.size
        print('    The number of Females in the dataset is:         {}\n'.format(num_female))
    else:
        print('    WARNING: No Gender information available in chosen city datafile...\n')
        
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        # Display counts of gender
        earliest_year = int(df['Birth Year'].min())
        print('    The earliest birth year in the dataset is:       {}'.format(earliest_year))
        recent_year = int(df['Birth Year'].max())
        print('    The most recent birth year in the dataset is:    {}'.format(recent_year))
        common_year = int(df['Birth Year'].mode().values[0])
        print('    The most common birth year in the dataset is:    {}'.format(common_year))
    else:
        print('    WARNING: No Birth Year information available in chosen city datafile...')


    print("This took %.3f seconds.\n" % (time.time() - start_time))

    
def raw_data(df):
    """Displays raw data five lines at a time upon request by the user."""

    raw = input('Would you like to see five lines of the raw data from the dataset (y/n): ')

    if raw.lower() == 'y':
        pos = 0
        
        while True:
            print(df.iloc[pos:pos+5])
            pos += 5
            
            raw = input('Would you like to see five more lines of the raw data from the dataset (y/n): ')
            if raw.lower() != 'y':
                break
        
    print()
    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)
        
        restart = input('Would you like to restart (y/n): ')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
