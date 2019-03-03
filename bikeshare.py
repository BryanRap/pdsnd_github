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
    # initializing lists to check against for accurate input 
    city_list = ['chicago', 'new york city', 'washington']
    month_list = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
    day_list = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    
    # Initial prompt to the user to show the program has started
    print('Hello! Let\'s explore some US bikeshare data!\n')
    
    # Get user input for the city to analyize, loop until the city entered is confirmed to be in the list, otherwise prompt an error and try again
    while True:
        city = input('Lets get started by picking the city to explore, you can choose from "chicago", "new york city", or "washington", enter one of them: ')
        print()
        if city.lower() in city_list:
            break   
        else:
            print('Oops, looks like you entered the wrong input, lets try again.\n ')
                                 
    # Get user input for the month to analyize, loop until the month value is confirmed correct
    while True:
        month = input('Next, lets pick the month to look at, or input "all" (january to june are available): ')
        print()
        if month.lower() in month_list:
            break
        else:
            print('Hmmm, we were expecting a different input, maybe check your spelling?  Lets try again.\n ')
            

    # Get user input for the day of the week to analyize, loop until the day value is confirmed correct
    while True:
        day = input('Lastly, lets pick the day to review, you can input "all" or pick a day (monday, tuesday, etc): ')
        print()
        if day.lower() in day_list:
            break
        else:
            print('Darn, looks like that wasnt what we were expecting for input, try again.\n ')
                    
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
    df = pd.read_csv(CITY_DATA[city.lower()])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week, and hour from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day of Week'] = df['Start Time'].dt.weekday_name
    df['Hour'] = df['Start Time'].dt.hour
    
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month.lower()) + 1
    
        # filter by month to create the new dataframe
        df = df[df['Month']==month]

    # filter by day of week if applicable
    if day != 'all':
                
        # filter by day of week to create the new dataframe
        df = df[df['Day of Week']==day.title()]
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    
    # Dictionary for month number to month name conversion
    month_dict = {1 : "January", 2 : "February", 3 : "March", 4 : "April", 5 : "May", 6 : "June"}
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # If all months are selected, print the most common month
    if len(df['Month'].unique()) > 1:
        month_list = df['Month'].value_counts().keys().tolist()
        most_common_month = month_dict[month_list[0]]
        print('The most common month of travel is: ', most_common_month)

    # If all days are selected, print the most common day
    if len(df['Day of Week'].unique()) > 1:
        day_list = df['Day of Week'].value_counts().keys().tolist()
        most_common_day = day_list[0]
        print('The most common day of travel is: ', most_common_day)     
                  
    # Prints the most common start hour
    hour_list = df['Hour'].value_counts().keys().tolist()
    most_common_hour = hour_list[0]
    print('The most common time to travel is: ', most_common_hour, ':00 hours')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    input('Please press enter to continue...')

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Prints the most commonly used start station
    start_station_list = df['Start Station'].value_counts().keys().tolist()
    print('The most common place to start a trip is: ', start_station_list[0])

    # Prints the most commonly used end station
    end_station_list = df['End Station'].value_counts().keys().tolist()
    print('The most common place to end a trip is: ', end_station_list[0])

    # Creates a new DataFrame with the count of the number of similiar start and end locations
    sub_df = df.groupby(['Start Station', 'End Station']).size().reset_index(name='Count')
    
    # Filters the DataFrame to only a single row based on the max number of trips   
    most_trips = sub_df[sub_df.Count == sub_df['Count'].max()]

    # Prints a statement indicating the which is the most common Start/End combo and the number of trips taken
    print('\nThe most common combination of Start and End Stations are: ')
    print('Start Station: {} & End Station: {} with {} trips completed'.format(most_trips.iloc[0]['Start Station'], most_trips.iloc[0]['End Station'], most_trips.iloc[0]['Count']))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
          
    input('Please press enter to continue...')      

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Calculate the total trip time
    total_time = df['Trip Duration'].sum()
    
    # Calculate the number of years and remainder
    years = int(total_time / (365*24*60*60))
    leftover_days = total_time % (365*24*60*60)
        
   # Calculate the number of days and remainder
    days = int(leftover_days / (24*60*60))
    leftover_hours = leftover_days % (24*60*60)
    
    # Calculate the number of hours and remainder
    hours = int(leftover_hours / (60*60))
    leftover_min = leftover_hours % (60*60)

    # Calculate the number of minues
    minutes = int(leftover_min / 60)
    
    # Print the output based on the first non zero value
    if years > 0:
        print('The cumulative trip time is {} years, {} days, {} hours, and {} min!'.format(years, days, hours, minutes))
    elif days > 0:
        print('The cumulative trip time is {} days, {} hours, and {} min!\n'.format(days, hours, minutes))
    else:
        print('The cumulative trip time is {} hours and {} minutes!'.format(hours, minutes))
    
    # Calculate the mean travel time
    avg_time = df['Trip Duration'].mean()

    # Determine the number of minutes and seconds
    avg_min = int(avg_time / 60)
    avg_sec = int(avg_time % 60)
    
    # Print the average trip time in minutes and seconds
    print('The average trip time is {} minutes and {} seconds!'.format(avg_min, avg_sec))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
          
    input('Please press enter to continue...')
          
def user_stats(df):
    """Displays statistics on bikeshare users, checks to confirm data is available before outputting."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The breakdown of user types is:')
    print(df['User Type'].value_counts().to_frame(), '\n')
    
    try:
        # Display counts of gender
        print('The breakdown of gender is:')      
        print(df.dropna(axis=0)['Gender'].value_counts().to_frame(), '\n')

        # Display earliest, most recent, and most common year of birth
        print('The most common birth year is: ', df.dropna(axis=0)['Birth Year'].mode()[0])
        print('The earliet birth year is: ', df.dropna(axis=0)['Birth Year'].min())
        print('The most recent birth year is: ', df.dropna(axis=0)['Birth Year'].max())
      
    except:
        print("\nOops, looks like there is no data for gender or birth year, moving on!") 
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    input('Please press enter to continue...')      
          
def raw_data_output(df):
    """Displays raw data from the csv files, prompts user for how much information to display"""
    print('\nOutputting raw data for review:\n')
    
    x=0
    while True:
        print(df.iloc[x:x+5])
        more_data = input('Do you want to see more data? (y/n)')
        if more_data == 'y':
            x += 5
            print()
        else:
            break
                             
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data_output(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
