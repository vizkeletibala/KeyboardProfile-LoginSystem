import pandas as pd
import numpy as np
import math
import json
from scipy.stats import t

def calculatePressTimes(key_down_user_data, key_up_user_data, username, inputId):
    key_press_times = {}
    key_down_user_data.pop('Enter')
    for key in key_down_user_data:
        if key in key_up_user_data:
            key_press_times[key] = abs(key_up_user_data[key] - key_down_user_data[key])

    differenceData = {'Username': username, "InputID": inputId}
    differenceData.update(key_press_times)
    print("Press time for keys:")
    print(differenceData)
    return differenceData


def calculateTimeBetweenKeys(key_down_user_data, username, inputId):

    key_order = ['k', 'e', 'y', 'b', 'o', 'a', 'r', 'd', 'i', 's', 't']

    time_between_keys = {}

    # Iterate over the keys in the predefined order
    for i in range(len(key_order) - 1):
        current_key = key_order[i]
        next_key = key_order[i + 1]
        # Calculate the time difference between consecutive keys
        time_difference = abs(key_down_user_data[next_key] - key_down_user_data[current_key])
        # Store the time difference for the current key pair
        time_between_keys[current_key + '-' + next_key] = time_difference

    differenceData = {'Username': username, "InputID": inputId}
    differenceData.update(time_between_keys)    

    print("Time between keys:")
    print(differenceData)
    return differenceData

def calculateMeanBetweenKeyTimes(username, excel_file='resources/BetweenKeysData.xlsx'):

    #columns = ["k-e", "e-y", "y-b",	"b-o",	"o-a", "a-r",	"r-d",	"d-i",	"i-s",	"s-t"]
    try:
        # Read the Excel file
        df = pd.read_excel(excel_file)
        times_data= []
        result_dict = {'k-e': 0, 'e-y': 0, 'y-b': 0, 'b-o': 0, 'o-a': 0, 'a-r': 0, 'r-d': 0, 'd-i': 0, 'i-s': 0, 's-t': 0}
        # Filter rows for the specified username
        user_df = df[df['Username'] == username]
        for i in range(user_df.shape[0]):
            times_data.append({column: user_df[column].iloc[i] for column in result_dict.keys()})
            for column in result_dict.keys():
                result_dict[column] = result_dict[column] + times_data[i][column]

        for column in result_dict.keys():
            result_dict[column] = result_dict[column] / len(times_data)

        return result_dict
    except Exception as e:
        print(f"Error: {e}")
        return {}
    
def calculateMeanPressTimes(username, excel_file='resources/KeyPressData.xlsx'):
    try:
        # Read the Excel file
        df = pd.read_excel(excel_file)
        times_data= []
        result_dict = {'k': 0, 'e': 0, 'y': 0, 'b': 0, 'o': 0, 'a': 0, 'r': 0, 'd': 0, 'i': 0, 's': 0, 't': 0}
        # Filter rows for the specified username
        user_df = df[df['Username'] == username]
        for i in range(user_df.shape[0]):
            times_data.append({column: user_df[column].iloc[i] for column in result_dict.keys()})
            for column in result_dict.keys():
                result_dict[column] = result_dict[column] + times_data[i][column]

        for column in result_dict.keys():
            result_dict[column] = result_dict[column] / len(times_data)

        return result_dict
    except Exception as e:
        print(f"Error: {e}")
        return {}

def calculateStandardDeviationBetweenKeyTimes(username, excel_file='resources/BetweenKeysData.xlsx'):
    try:
        # Read the Excel file
        df = pd.read_excel(excel_file)
        times_data= []
        columns = {'k-e': 0, 'e-y': 0, 'y-b': 0, 'b-o': 0, 'o-a': 0, 'a-r': 0, 'r-d': 0, 'd-i': 0, 'i-s': 0, 's-t': 0}
        # Filter rows for the specified username
        user_df = df[df['Username'] == username]
        for i in range(user_df.shape[0]):
            times_data.append({column: user_df[column].iloc[i] for column in columns.keys()}) # parse the data into a dictionary

        result_std = {column: np.std([times_data[i][column] for i in range(len(times_data))]) for column in columns.keys()} # calculate the standard deviation for each key pair

        return result_std
    except Exception as e:
        print(f"Error: {e}")
        return {}

def calculateStandardDeviationPressTimes(username, excel_file='resources/KeyPressData.xlsx'):
    try:
        # Read the Excel file
        df = pd.read_excel(excel_file)
        times_data= []
        columns = {'k': 0, 'e': 0, 'y': 0, 'b': 0, 'o': 0, 'a': 0, 'r': 0, 'd': 0, 'i': 0, 's': 0, 't': 0}
        # Filter rows for the specified username
        user_df = df[df['Username'] == username]
        for i in range(user_df.shape[0]):
            times_data.append({column: user_df[column].iloc[i] for column in columns.keys()})

        result_std = {column: np.std([times_data[i][column] for i in range(len(times_data))]) for column in columns.keys()}

        return result_std
    except Exception as e:
        print(f"Error: {e}")
        return {}

def calculateConfidenceInterval(username, excel_file, confidence_level=0.95):
    if (excel_file == 'resources/KeyPressData.xlsx'):

        try:
            print("Calculating confidence interval for key press times")

            df = pd.read_excel(excel_file)
            user_data = df[df['Username'] == username]
            entry_count = len(user_data)
            # Calculate the mean keypress times
            mean_keypress_times = calculateMeanPressTimes(username)
            standard_deviation_press_times = calculateStandardDeviationPressTimes(username)

            # Initialize dictionary to store confidence intervals for each key
            confidence_intervals = {}

            # Calculate confidence interval for each key
            for key, mean_time in mean_keypress_times.items():
                # Get the standard deviation for this key
                std_dev = standard_deviation_press_times[key]

                # Calculate the standard error
                standard_error = std_dev / entry_count ** 0.5

                # Calculate the degrees of freedom
                degrees_of_freedom = entry_count - 1

                # Calculate the t-value for the given confidence level and degrees of freedom
                t_value = t.ppf((1 + confidence_level) / 2, degrees_of_freedom)

                # Calculate the margin of error
                margin_of_error = t_value * standard_error

                # Calculate the confidence interval
                confidence_interval_lower = mean_time - margin_of_error
                confidence_interval_upper = mean_time + margin_of_error

                # Store the confidence interval for this key
                confidence_intervals[key] = (confidence_interval_lower, confidence_interval_upper)

            return confidence_intervals

        except Exception as e:
            print(f"Error: {e}")
            return None, None
        
    elif (excel_file == 'resources/BetweenKeysData.xlsx'):
        print("Calculating confidence interval for time between keys")
        try:
            df = pd.read_excel(excel_file)
            user_data = df[df['Username'] == username]
            entry_count = len(user_data)
            # Calculate the mean time between keys
            mean_time_between_keys = calculateMeanBetweenKeyTimes(username)
            standard_deviation_between_keys = calculateStandardDeviationBetweenKeyTimes(username)

            # Initialize dictionary to store confidence intervals for each key pair
            confidence_intervals = {}

            # Calculate confidence interval for each key pair
            for key_pair, mean_time in mean_time_between_keys.items():
                # Get the standard deviation for this key pair
                std_dev = standard_deviation_between_keys[key_pair]

                # Calculate the standard error
                standard_error = std_dev / entry_count ** 0.5

                # Calculate the degrees of freedom
                degrees_of_freedom = entry_count - 1

                # Calculate the t-value for the given confidence level and degrees of freedom
                t_value = t.ppf((1 + confidence_level) / 2, degrees_of_freedom)

                # Calculate the margin of error
                margin_of_error = t_value * standard_error

                # Calculate the confidence interval
                confidence_interval_lower = mean_time - margin_of_error
                confidence_interval_upper = mean_time + margin_of_error

                # Store the confidence interval for this key pair
                confidence_intervals[key_pair] = (confidence_interval_lower, confidence_interval_upper)

            return confidence_intervals

        except Exception as e:
            print(f"Error: {e}")
            return None, None
    else:
        print("Error: Invalid Excel file")
        return None, None
    

    
def calculateVectorDifference(baseline, sample):
    if len(baseline) != len(sample):
        print("Error: Vectors must have the same length.")
        return None

    result = 0
    for i in range(len(baseline)):
        result += (float(baseline[i]) - float(sample[i])) ** 2

    return math.sqrt(result)

def calculateUserGuess(keypress, betweenkeys, user, json_file='resources/ConfidenceIntervals.json'):
    # Calculate the possibilty of the user being the registered user
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        usernames = list(data.keys())
        if user not in usernames:
            return None, None
        
        most_likely_user = None
        interval_pass_counter = 0
        for username in usernames:
            user_intervals = data.get(username)
            if user_intervals:
                between_keys_intervals = user_intervals.get('BetweenKeysInterval', {})
                key_press_intervals = user_intervals.get('KeyPressInterval', {})
                between_results, between_counter = checkValuesWithinIntervals(betweenkeys, between_keys_intervals)
                keypress_results, keypress_counter = checkValuesWithinIntervals(keypress, key_press_intervals)
                print("Between keys results:", between_results)
                print("Keypress results:", keypress_results)
                if between_counter + keypress_counter > interval_pass_counter:
                    interval_pass_counter = between_counter + keypress_counter
                    most_likely_user = username
            else:
                print(f"No data found for user '{username}' in the JSON file.")
                return None, None
        
        return most_likely_user, interval_pass_counter
    except Exception as e:
        print(f"Error: {e}")
        return None, None

def checkValuesWithinIntervals(data, intervals):
    # Dictionary to store whether each key's value is within its confidence interval
    within_intervals = {}
    within_counter = 0
    # Iterate over each key and value pair in the data
    for key, value in data.items():
        # Check if the key is present in the intervals dictionary
        if key in intervals:
            # Get the confidence interval for the key
            interval = intervals[key]
            # Check if the value falls within the confidence interval bounds
            if interval[0] <= value <= interval[1]:
                within_intervals[key] = True
                within_counter += 1
            else:
                within_intervals[key] = False
        else:
            #print(f"No confidence interval found for key '{key}'")
            within_intervals[key] = None
    
    return within_intervals, within_counter


