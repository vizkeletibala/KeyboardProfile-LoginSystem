import pandas as pd
import numpy as np
import math
import json
from scipy.stats import t

def calculatePressTimes(key_down_user_data, key_up_user_data, username, inputId):
    # Calculate the press time from keydown data and keyup data, by subtracting previous key down time from current key up time for a certain user.
    key_press_times = {}
    if 'Enter' in key_down_user_data:
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
    # Calculate the time between keys from keydown data, by subtracting previous key down time from current key down time for a certain user.
    key_order = ['k', 'e', 'y', 'b', 'o', 'a', 'r', 'd', 'i', 's', 't']

    time_between_keys = {}

    for i in range(len(key_order) - 1):
        current_key = key_order[i]
        next_key = key_order[i + 1]
        if  current_key in key_down_user_data and next_key in key_down_user_data:
            time_difference = abs(key_down_user_data[next_key] - key_down_user_data[current_key])
            time_between_keys[current_key + '-' + next_key] = time_difference
        else:
            # Print debug information about missing keys
            if current_key not in key_down_user_data:
                print(f"Key '{current_key}' not found in key_down_user_data")
                return None
            if next_key not in key_down_user_data:
                print(f"Key '{next_key}' not found in key_down_user_data")
                return None

    differenceData = {'Username': username, "InputID": inputId}
    differenceData.update(time_between_keys)    

    print("Time between keys:")
    print(differenceData)
    return differenceData

def calculateMeanBetweenKeyTimes(username, excel_file='resources/BetweenKeysData.xlsx'):
    # Calculate and store the average between keys time for each key for a certain user. 
    #columns = ["k-e", "e-y", "y-b",	"b-o",	"o-a", "a-r",	"r-d",	"d-i",	"i-s",	"s-t"]
    try:
        df = pd.read_excel(excel_file)
        times_data= []
        result_dict = {'k-e': 0, 'e-y': 0, 'y-b': 0, 'b-o': 0, 'o-a': 0, 'a-r': 0, 'r-d': 0, 'd-i': 0, 'i-s': 0, 's-t': 0}
        user_df = df[df['Username'] == username]
        for i in range(user_df.shape[0]):
            times_data.append({column: user_df[column].iloc[i] for column in result_dict.keys()})
            for column in result_dict.keys():
                result_dict[column] = result_dict[column] + times_data[i][column]

        for column in result_dict.keys():
            result_dict[column] = result_dict[column] / len(times_data)

        print("Mean calculated for Between Key Times.")
        print(result_dict)
        storeMeansInExcel(username, result_dict, 'resources/BetweenKeysMeansData.xlsx')
        return result_dict
    except Exception as e:
        print(f"Error: {e}")
        return {}
    
def calculateMeanPressTimes(username, excel_file='resources/KeyPressData.xlsx'):
    # Calculate and store the average press time for each key for a certain user
    try:
        df = pd.read_excel(excel_file)
        times_data= []
        result_dict = {'k': 0, 'e': 0, 'y': 0, 'b': 0, 'o': 0, 'a': 0, 'r': 0, 'd': 0, 'i': 0, 's': 0, 't': 0}
        user_df = df[df['Username'] == username]
        for i in range(user_df.shape[0]):
            times_data.append({column: user_df[column].iloc[i] for column in result_dict.keys()})
            for column in result_dict.keys():
                result_dict[column] = result_dict[column] + times_data[i][column]

        for column in result_dict.keys():
            result_dict[column] = result_dict[column] / len(times_data)  

        print("Mean calculated for Press Times:")
        print(result_dict)
        storeMeansInExcel(username, result_dict, 'resources/KeyPressMeansData.xlsx')
        return result_dict
    except Exception as e:
        print(f"Error: {e}")
        return {}
    

def storeMeansInExcel(username, data, filePath):
    # Store the data in an excel, overwrite if user already has means stored.
    try:
        try:
            existing_data = pd.read_excel(filePath, index_col=0, header=0)
        except FileNotFoundError:
            # If file does not exist, create an empty DataFrame with the correct structure
            columns = ['Username'] + list(data.keys())
            existing_data = pd.DataFrame(columns=columns).set_index('Username')

        for key, value in data.items():
            existing_data.loc[username, key] = value

        # Write the updated data back to the Excel file
        existing_data.to_excel(filePath, index=True)

        print('Data has been stored in Excel file: ' + filePath)
    except Exception as e:
        print(f"Error: {e}")
        return {}

def calculateStandardDeviationBetweenKeyTimes(username, excel_file='resources/BetweenKeysData.xlsx'):
    # Calculate the standard deviation od between keys time for certain user.
    try:
        df = pd.read_excel(excel_file)
        times_data= []
        columns = {'k-e': 0, 'e-y': 0, 'y-b': 0, 'b-o': 0, 'o-a': 0, 'a-r': 0, 'r-d': 0, 'd-i': 0, 'i-s': 0, 's-t': 0}
        user_df = df[df['Username'] == username]
        for i in range(user_df.shape[0]):
            times_data.append({column: user_df[column].iloc[i] for column in columns.keys()}) 

        result_std = {column: np.std([times_data[i][column] for i in range(len(times_data))]) for column in columns.keys()}

        return result_std
    except Exception as e:
        print(f"Error: {e}")
        return {}

def calculateStandardDeviationPressTimes(username, excel_file='resources/KeyPressData.xlsx'):
    # Calculate the standard deviation of press time for certain user.
    try:
        df = pd.read_excel(excel_file)
        times_data= []
        columns = {'k': 0, 'e': 0, 'y': 0, 'b': 0, 'o': 0, 'a': 0, 'r': 0, 'd': 0, 'i': 0, 's': 0, 't': 0}
        user_df = df[df['Username'] == username]
        for i in range(user_df.shape[0]):
            times_data.append({column: user_df[column].iloc[i] for column in columns.keys()})

        result_std = {column: np.std([times_data[i][column] for i in range(len(times_data))]) for column in columns.keys()}

        return result_std
    except Exception as e:
        print(f"Error: {e}")
        return {}

def calculateConfidenceInterval(username, excel_file, confidence_level=0.95):
    # Calculate an upper and lover interval limit for each key for KeyPress and BetweenKeys Data
    if (excel_file == 'resources/KeyPressData.xlsx'):
        try:
            print("Calculating confidence interval for key press times")

            df = pd.read_excel(excel_file)
            user_data = df[df['Username'] == username]
            entry_count = len(user_data)
            mean_keypress_times = calculateMeanPressTimes(username)
            standard_deviation_press_times = calculateStandardDeviationPressTimes(username)

            confidence_intervals = {}

            for key, mean_time in mean_keypress_times.items():

                std_dev = standard_deviation_press_times[key]
                standard_error = std_dev / entry_count ** 0.5
                degrees_of_freedom = entry_count - 1

                t_value = t.ppf((1 + confidence_level) / 2, degrees_of_freedom)

                margin_of_error = t_value * standard_error

                confidence_interval_lower = mean_time - margin_of_error
                confidence_interval_upper = mean_time + margin_of_error

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
            mean_time_between_keys = calculateMeanBetweenKeyTimes(username)
            standard_deviation_between_keys = calculateStandardDeviationBetweenKeyTimes(username)

            confidence_intervals = {}

            for key_pair, mean_time in mean_time_between_keys.items():
                std_dev = standard_deviation_between_keys[key_pair]

                standard_error = std_dev / entry_count ** 0.5

                degrees_of_freedom = entry_count - 1
                t_value = t.ppf((1 + confidence_level) / 2, degrees_of_freedom)

                margin_of_error = t_value * standard_error

                confidence_interval_lower = mean_time - margin_of_error
                confidence_interval_upper = mean_time + margin_of_error
                confidence_intervals[key_pair] = (confidence_interval_lower, confidence_interval_upper)

            return confidence_intervals

        except Exception as e:
            print(f"Error: {e}")
            return None, None
    else:
        print("Error: Invalid Excel file")
        return None, None
    

    
def calculateVectorDifference(baseline, sample):
    # Defining a vector difference based on pythagorean theorem.
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
        interval_pass_counter = 3
        for username in usernames:
            user_intervals = data.get(username)
            if user_intervals:
                between_keys_intervals = user_intervals.get('BetweenKeysInterval', {})
                key_press_intervals = user_intervals.get('KeyPressInterval', {})
                between_results, between_counter = checkValuesWithinIntervals(betweenkeys, between_keys_intervals)
                keypress_results, keypress_counter = checkValuesWithinIntervals(keypress, key_press_intervals)
                print("Between keys results for user:", user, between_results)
                print("Keypress results for user:", user,keypress_results)
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
    # Check and calculate the number of intervals in which the data fits in.  
    within_intervals = {}
    within_counter = 0
    for key, value in data.items():
        if key in intervals:
            interval = intervals[key]
            if interval[0] <= value <= interval[1]:
                within_intervals[key] = True
                within_counter += 1
            else:
                within_intervals[key] = False
        else:
            within_intervals[key] = None
    
    return within_intervals, within_counter

def calculateAllUserMeans(excel_file):
    # Determine the number of columns to process based on the file path
    if excel_file == "resources/BetweenKeysData.xlsx":
        num_columns = 10
    elif excel_file == "resources/KeyPressData.xlsx":
        num_columns = 11
    else:
        raise ValueError("Invalid file path")
    
    print("Entered func")
    print(f"Reading Excel file: {excel_file}")
    df = pd.read_excel(excel_file)
        
    print(f"Excel file read successfully: {df.shape} rows and columns")

    users = df['Username'].unique()
    print(users)

    user_means = {key: [] for key in df.columns[2:2 + num_columns]}
    # Iterate over each user to calculate the mean time for each key
    for user in users:
        user_data = df[df['Username'] == user].iloc[:, 2:2 + num_columns]
        for key in user_data.columns:
            user_means[key].append(user_data[key].mean())

    # Calculate the average of averages for each key
    overall_means = {key: sum(means) / len(means) for key, means in user_means.items()}
    print("Overall means: ", overall_means)

    return overall_means
