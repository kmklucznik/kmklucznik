import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv'}

months=('january','february','march','april','may','june')

weekdays=('sunday','monday','tuesday','wednesday','thursday','friday','saturday')

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print("If at any time you wish to exit please type end.")

    false_count = 0

    while false_count >= 0:
        city=str(input("\n Pick the city(ies) for which you would like to see data for separated by commas: Chicago, New York City, Washington.\n"))
        # splits, makes lower case and Remove extra white space if 2 or more cities entered
        city = [i.strip().lower() for i in city.split(',')]
        if 'end' in city:
            print("Thank you, goodbye.")
            raise SystemExit
        else:
            for i in city:
                if i not in CITY_DATA.keys():
                    false_count += 1
                    print(i)
                    print(" is not valid. Please try again. \n")
                else:
                    # if i in CITY_DATA.keys():
                    print(i)
                    print(" is valid.\n")
            if false_count >= 1:
                false_count = 0
                continue
            else:
                break

    while false_count >= 0:
        month= str(input("\n Please which month(s) from January to June you would to see data for seperated by commas: \n"))
        month = [i.strip().lower() for i in month.split(',')]
        if 'end' in month:
            print("Thank you, goodbye.")
            raise SystemExit
        else:
            for i in month:
                if i not in months:
                    false_count +=1
                    print(i)
                    print(" is not valid. Please try again. \n")
                else:
                    print(i)
                    print(" is valid.\n")

            if false_count >= 1:
                false_count = 0
                continue
            else:
                break

    day=str(input("\n Please choose the day(s) of the week you would like to see data for seperated by commas: \n"))
    day = [i.strip().lower() for i in day.split(',')]
    if 'end' in day:
        print("Thank you, goodbye.")
        raise SystemExit
    else:
        for i in day:
            if i in weekdays:
                print(i)
                print(" is valid. \n")
            else:
                print(i)
                print(" is not valid. Please try again. \n")

    print("Filtering your selection...")
    print()
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

    if isinstance(city, list):
        df = pd.concat(map(lambda city: pd.read_csv(CITY_DATA[city]), city),sort=True)
        # reorganize DataFrame columns after a city concat
        try:
            df = df.reindex(columns=['Unnamed: 0', 'Start Time', 'End Time',
                                     'Trip Duration', 'Start Station',
                                     'End Station', 'User Type', 'Gender',
                                     'Birth Year'])
        except:
            pass
    else:
        df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime type
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day_of_Week'] = df['Start Time'].dt.day_name()
    df['Hour'] = df['Start Time'].dt.hour


    print (df['Month'])
    print (df['Day_of_Week'])
    # filter the data according to month and weekday into two new DataFrames
    if isinstance(month, list):
        df = pd.concat(map(lambda month: df[df['Month'] == (months.index(month)+1)], month))
    else:
        df = df[df['Month'] == (months.index(month)+1)]

    if isinstance(day, list):
        df = pd.concat(map(lambda day: df[df['Day_of_Week'] == (day.title())], day))
    else:
        df = df[df['Day_of_Week'] == day.title()]



    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # look_up dictionary
    month_look_up = {'1': 'January', '2': 'February', '3': 'March', '4': 'April', '5': 'May',
        '6': 'June', '7': 'July', '8': 'August', '9': 'September', '10': 'October', '11': 'November', '12': 'December'}


    # display the most common month
    popular_month = df['Month'].mode()[0]
    month_in_string = month_look_up[str(popular_month)]
    print("1. The most common month was: ", month_in_string)

    # display the most common day of week
    popular_day = df['Day_of_Week'].mode()[0]
    print("2. The most common day of the week was: {}".format(popular_day))

    # display the most common start hour
    popular_hour = df['Hour'].mode()[0]
    print('3. The most common start hour was:', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station

    start_station = df['Start Station'].mode()[0]
    print("Most common start station was: '{}'.".format(start_station))

    # display most commonly used end station

    end_station = df['End Station'].mode()[0]
    print("Most common end station was: '{}'.".format(end_station))

    # display most frequent combination of start station and end station trip

    pair_final = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).reset_index(name="counts")

    frequent_start_pair = pair_final['Start Station'][0]
    frequent_end_pair = pair_final['End Station'][0]

    print("The most frequent combination is '{}' to start and '{}' to end.".format(frequent_start_pair, frequent_end_pair))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()

    t2 = total_travel_time.astype('float64', copy=False)
    time_in_duration = dt.timedelta(seconds=t2)

    print("The total travel time in seconds is: '{}' which converts to '{}' in duration.".format(total_travel_time, time_in_duration))

    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()

    mean_travel_duration = dt.timedelta(seconds=mean_travel_time)
    print("Mean travel time is: '{}' seconds which converts to '{}' in duration.".format(mean_travel_time, mean_travel_duration))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type_count = df["User Type"].value_counts()
    print(user_type_count)

    if df["Gender"].count() < 1:
        print("\n No gender data exists in this dataset.")
    else:
        gender_count = df["Gender"].value_counts()
        # to count null values
        # Reference: https://stackoverflow.com/questions/26266362/how-to-count-the-nan-values-in-a-column-in-pandas-dataframe
        nan_values = df["Gender"].isna().sum()
        print("\n Counts by Gender: \n{}\n \n*Note: there were '{}' NaN values for 'Gender' column \n".format(
            gender_count, nan_values))

    # Display earliest, most recent, and most common year of birth
    if df["Birth Year"].count() < 1:
        print("\n No birth year data exists in this data set. \n")
    else:
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()[0]
        print("\n Earliest birth year: '{}'. \nMost recent birth year: '{}'. \nMost common birth year: '{}'.".format(
            earliest, most_recent, most_common))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):

    # initial input!
    display_raw_input = str(input("\nWould you like to see individual raw data? Enter 'yes' or 'no'\n").strip().lower())
    if display_raw_input in ("yes", "y"):
        i = 0

        # use while loop for the inputs that you want repeated!
        # thus should start here, not at the beginning of the code

        while True:
            # check if i is out of bounds, if upper limit is out of bounds,
            # then print from lower limit to length of dataframe rows
            if (i + 5 > len(df.index) - 1):
                # remember that the slicing is lower bound inclusive and upper bound exclusive!!
                # thus upper bound should be (len(df.index) --> won't print out that upper bound bc its exclusive)
                print(df.iloc[i:len(df.index), :])
                print("You've reached the end of the rows")
                break

            # if i is not out of bounds, then just print the dataframe normally
            print(df.iloc[i:i+5, :])
            i += 5

            # program temporarily halts at the input!
            # thus while loop does not get executed 100000 times (exaggerated) a second lol
            show_next_five_input = str(input("\nWould you like to see the next 5 rows? Enter 'yes' or 'no'\n").strip().lower())
            if show_next_five_input not in ("yes", "y"):
                break # break out of while loop above
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
