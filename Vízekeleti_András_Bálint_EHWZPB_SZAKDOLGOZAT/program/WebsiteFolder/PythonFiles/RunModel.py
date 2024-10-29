from ModelCalculations import calculateMeanBetweenKeyTimes, calculatePressTimes, calculateTimeBetweenKeys, calculateMeanPressTimes, calculateVectorDifference, calculateAllUserMeans, calculateConfidenceInterval, calculateUserGuess
from openpyxl import Workbook
import numpy as np
import pandas as pd
import json
import sys
import random
import string

CONST_PASSWORD = 'keyboardist'

KEYPRESSTIMES = {}
BETWEENKEYSTIMES = {}
USER = ""
PASSWORD = ""

print('Python version:', sys.version)

print('Pandas version:', pd.__version__) 

def generateInputID():
    
    existing_numbers = set()
    with open("resources/inputIds.txt", 'r') as file:
        for line in file:
            number = line.strip()
            existing_numbers.add(number)
    file.close()

    def generateRandomWord():
        letters = string.ascii_lowercase
        random_word = ''.join(random.choice(letters) for _ in range(3))
        return random_word

    random_word = generateRandomWord()

    while True:
        random_number = str(random.randint(10000000, 99999999)) + random_word
        if random_number not in existing_numbers:
            with open("resources/inputIds.txt", 'a') as file:
                file.write(random_number + '\n')
                file.close()
            return random_number

def parseKeyData(input_key_data):

    key_data = {}
    for times in input_key_data:
        key = times['key']
        key_up_time = times.get('time', 0)
        key_data[key] = key_up_time
    return key_data

def createDataForCharts():

    BK_result_dict = calculateMeanBetweenKeyTimes(USER)
    KP_result_dict = calculateMeanPressTimes(USER)

    storeMeansInJSON(KP_result_dict, USER, 'resources/KeyPressChartData.json')
    storeMeansInJSON(BK_result_dict, USER, 'resources/BetweenKeysChartData.json')   # Store the mean of keypress and between key times in a json file for the charts
    
    BK_all_user_mean = calculateAllUserMeans('resources/BetweenKeysData.xlsx')
    KP_all_user_mean = calculateAllUserMeans('resources/KeyPressData.xlsx')

    storeMeansInJSON(BK_all_user_mean, 'AllUsers', 'resources/AllBetweenKeysChartData.json')
    storeMeansInJSON(KP_all_user_mean, 'AllUsers', 'resources/AllKeyPressChartData.json')

    print("Charts Data stored!")


def generateDataFrames(json_file):
    global KEYPRESSTIMES, BETWEENKEYSTIMES, USER, PASSWORD

    with open(json_file, 'r') as f:
        data = json.load(f)

    # Extract username, password, keyup, and keydown data
    username = data.get('username', '')
    USER = username
    password = data.get('password', '')
    PASSWORD = password
    email = data.get('email', '')
    keyup_data = data.get('keyup', [])
    keydown_data = data.get('keydown', [])

    # Check if the password is correct
    if password == CONST_PASSWORD:

        print('Correct password. Processing data...')

        # Generate a unique input ID that is the same for this instance of keyup and keydown data
        inputId = generateInputID()
        # Initialize dictionaries to store keyup and keydown data
        key_down_user_data = parseKeyData(keydown_data)
        print("Key down user data:")
        print(key_down_user_data)
        key_up_user_data = parseKeyData(keyup_data)
        print("Key up user data:")
        print(key_up_user_data)

        KEYPRESSTIMES = calculatePressTimes(key_down_user_data, key_up_user_data, username, inputId)
        BETWEENKEYSTIMES = calculateTimeBetweenKeys(key_down_user_data, username, inputId) # We can also calculate the time between keys here

        if BETWEENKEYSTIMES is None:
            return None

        # Create a dictionary to hold all keyboard data
        keyboard_data_up = {'Username': username, 'Email': email, "InputID": inputId}
        keyboard_data_up.update(key_up_user_data)
        keyboard_data_down = {'Username': username, 'Email': email, "InputID": inputId}
        keyboard_data_down.update(key_down_user_data)

        # Create a DataFrame from the keyboard data
        key_up_df = pd.DataFrame(keyboard_data_up, index=[0])
        key_down_df = pd.DataFrame(keyboard_data_down, index=[0])
        return (key_down_df, key_up_df)
    else:
        print('Invalid password. Please try again.')
        return None
    
def writeLoginResultToFile(username, login_result, xl_file_path='resources/LoginResults.xlsx', json_file_path='resources/LoginResult.json'):
    try:
        # Create a DataFrame to store the login result
        login_result_df = pd.DataFrame({'Username': [username], 'LoginResult': [login_result]})
        
        storeData(login_result_df, xl_file_path)

        data = {'login result': login_result}

        with open(json_file_path, 'w') as f:
            json.dump(data, f)
        print(f"Boolean variable '{login_result}' successfully written to '{json_file_path}'.")
    except Exception as e:
        print(f"Error: {e}")
    
def getUniqueUsernames(json_file_path):
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
        
        result = [username for username, count in data.items() if count >= 10]
        return result
    except Exception as e:
        print(f"Error: {e}")
        return []
    
def countRowsByUsername(username, excel_file="resources/KeyPressData.xlsx"):
    try:
        df = pd.read_excel(excel_file)
        # Filter the rows where the username matches the given parameter
        filtered_df = df[df['Username'] == username]
        row_count = len(filtered_df)
            
        return row_count
    except Exception as e:
        print(f"Error: {e}")
        return 0
    
def storeData(differenceData, filePath):
    
    existing_data = pd.read_excel(filePath)
    if differenceData.empty:
        print('Data is empty. Nothing to store in Excel file.')
    else:
        excel_file = filePath
        existing_data = pd.concat([existing_data, differenceData], axis=0, sort=False)
        existing_data.to_excel(excel_file, index=False)
        print('Data has been stored in Excel file: ' + excel_file)

def getSampleVector():

    keypressCopy = KEYPRESSTIMES
    betweenkeysCopy = BETWEENKEYSTIMES

    if 'Backspace' in keypressCopy.keys():
            keypressCopy.pop('Backspace') # Remove the backspace key from the dictionary

    keypressCopy.pop('Username') # Remove the username from the dictionary
    keypressCopy.pop('InputID') # Remove the input ID from the dictionary

    betweenkeysCopy.pop('Username')
    betweenkeysCopy.pop('InputID')

    return (np.array(list(keypressCopy.values())), np.array(list(betweenkeysCopy.values())))

def getBaselineVector(user):

    KPdf = pd.read_excel('resources/KeyPressMeansData.xlsx')
    BKdf = pd.read_excel('resources/BetweenKeysMeansData.xlsx')

    user_row = KPdf[KPdf['Username'] == user]
    presstimes = user_row.iloc[:, 1:].values.flatten()

    BK_row = BKdf[BKdf['Username'] == user]
    betweenkeys = BK_row.iloc[:, 1:].values.flatten()

    return (presstimes, betweenkeys)

def storeMeansInJSON(data, username, json_file):
    try:
        with open(json_file, 'w') as f:
            json.dump({username: data}, f)
        print("Means stored in: ", json_file)

    except Exception as e:
        print(f"Error: {e}")
        return {}

def storeConfidenceIntervalsInJSON(username, betweenKeysInterval, keyPressInterval, json_file="resources/ConfidenceIntervals.json"):
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file does not exist or is empty, initialize data as an empty dictionary
        data = {}

    data[username] = {'BetweenKeysInterval': betweenKeysInterval, 'KeyPressInterval': keyPressInterval}
    print("USer confidence intervals:", data)

    with open(json_file, 'w') as f:
        json.dump(data, f)

def loginSequence(df_result_tuple):
     global KEYPRESSTIMES, BETWEENKEYSTIMES, USER, PASSWORD

     userEntries = countRowsByUsername(USER)
     if userEntries > 9 and PASSWORD == CONST_PASSWORD:

        login_result = False
        print("User has more than 10 entries in the database.")
        print('Attempting to authenticate user...')

        sample_vector = getSampleVector()
        print("Sample Vector for user: ", USER)
        print(sample_vector)

        differences = []
        
        min_difference = 10000000
        # Going through all the users in the database to see which one is the closest to the sample
        for user in getUniqueUsernames('resources/registry.json'):

            baseline_vector = getBaselineVector(user)
            print("Baseline Vector for user: ", user)
            print(baseline_vector)

            # Calculate the vector difference between the sample and baseline vectors
            presstime_vector_difference = calculateVectorDifference(baseline_vector[0], sample_vector[0])
            print("Press Time Vector Difference for user: ", user)
            print(presstime_vector_difference)

            betweenkey_vector_difference = calculateVectorDifference(baseline_vector[1], sample_vector[1])
            print("Between Key Vector Difference for user: ", user)
            print(betweenkey_vector_difference)

            difference = presstime_vector_difference * betweenkey_vector_difference
            differences.append((user, difference))

            if difference < min_difference:
                min_difference = presstime_vector_difference * betweenkey_vector_difference

        sorted_differences = sorted(differences, key=lambda x: x[1])
        if len(sorted_differences) >= 2:
            closest_user = sorted_differences[0][0]
            second_closest_user = sorted_differences[1][0]
            third_closest_user = sorted_differences[2][0]
            closest_difference = sorted_differences[0][1]
            second_closest_difference = sorted_differences[1][1]
        else:
            closest_user = sorted_differences[0][0]
            closest_difference = sorted_differences[0][1]
            third_closest_user = None
            second_closest_user = None
            second_closest_difference = None

        print("User: ", USER)
        print("Closest User: ", closest_user)
        print("Second Closest User: ", second_closest_user)
        print("Third Closest User: ", third_closest_user)
        print("Closest Difference: ", closest_difference)
        print("Second Closest Difference: ", second_closest_difference)
        guessUser = calculateUserGuess(KEYPRESSTIMES, BETWEENKEYSTIMES, USER)[0]
        difference = min_difference
        print("Guess User: ", guessUser)
        print("Difference: ", difference)
        # First we check if the confidence intervals based check found the correct user
        login_result = guessUser == USER
        # If the login was succesful we also store the data in the excel files and create the data for the chart statistics.
        if login_result: 
            print("User has been successfully authenticated.")

            new_down_df = df_result_tuple[0]
            new_up_df = df_result_tuple[1]

            inputId = generateInputID()

            storeData(new_down_df, 'resources/DownData.xlsx')
            storeData(new_up_df, 'resources/UpData.xlsx')

            betweenkeydata = {'Username': USER, "InputID": inputId}
            keypressdata = {'Username': USER, "InputID": inputId}
            betweenkeydata.update(BETWEENKEYSTIMES)
            keypressdata.update(KEYPRESSTIMES)

            storeData(pd.DataFrame(keypressdata, index=[0]), 'resources/KeyPressData.xlsx')
            storeData(pd.DataFrame(betweenkeydata, index=[0]), 'resources/BetweenKeysData.xlsx')

            writeLoginResultToFile(USER, login_result)
            createDataForCharts()
        # If the condifedence interval based check doesnt find the user, we use the vector difference based check
        elif USER == second_closest_user or USER == closest_user:
            login_result = True
            print("User has been successfully authenticated.")

            new_down_df = df_result_tuple[0]
            new_up_df = df_result_tuple[1]
            inputId = generateInputID()

            storeData(new_down_df, 'resources/DownData.xlsx')
            storeData(new_up_df, 'resources/UpData.xlsx')

            betweenkeydata = {'Username': USER, "InputID": inputId}
            keypressdata = {'Username': USER, "InputID": inputId}
            betweenkeydata.update(BETWEENKEYSTIMES)
            keypressdata.update(KEYPRESSTIMES)

            storeData(pd.DataFrame(keypressdata, index=[0]), 'resources/KeyPressData.xlsx')
            storeData(pd.DataFrame(betweenkeydata, index=[0]), 'resources/BetweenKeysData.xlsx')

            writeLoginResultToFile(USER, login_result)
            createDataForCharts()
        # If none of the checks 
        else:
            writeLoginResultToFile(USER, login_result)

     else:
        login_result = False
        print("User has less than 10 entries in the database.")
        writeLoginResultToFile(USER, login_result)
        
def registerSequence(df_result_tuple):

    if df_result_tuple is None:
        print("Something went wrong while parsing the data. Please try again.")
   
    new_down_df = df_result_tuple[0]
    new_up_df = df_result_tuple[1]

    storeData(new_down_df, 'resources/DownData.xlsx')
    storeData(new_up_df, 'resources/UpData.xlsx')

    inputId = generateInputID()

    betweenkeydata = {'Username': USER, "InputID": inputId}
    keypressdata = {'Username': USER, "InputID": inputId}
    betweenkeydata.update(BETWEENKEYSTIMES)
    keypressdata.update(KEYPRESSTIMES)

    storeData(pd.DataFrame(keypressdata, index=[0]), 'resources/KeyPressData.xlsx')
    storeData(pd.DataFrame(betweenkeydata, index=[0]), 'resources/BetweenKeysData.xlsx')

    if incrementUserRegistration("resources/registry.json", USER): # Increment the number of registrations for the user and if there is more than 10 entries in the database we calculate the means

        calculateMeanBetweenKeyTimes(USER) # Calculate the mean between key times for the user
        calculateMeanPressTimes(USER)  # Calculate the mean of key press times for the user

        kpIntervals = calculateConfidenceInterval(USER, 'resources/KeyPressData.xlsx')
        bkIntervals = calculateConfidenceInterval(USER, 'resources/BetweenKeysData.xlsx')

        storeConfidenceIntervalsInJSON(USER, bkIntervals, kpIntervals)
        print("User means have been calculated.")
    else:
        print("User has less than 10 entries in the database.")

def incrementUserRegistration(json_file, username):
    try:
        with open(json_file, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    data[username] = data.get(username, 0) + 1
    with open(json_file, 'w') as f:
        json.dump(data, f)
    return data[username] > 9 and 20 > data[username] 

def main():

    operation = ""
    if len(sys.argv) > 1:
        print("Command-line arguments are provided.")
        print("Arguments:", sys.argv[1:])
        operation = sys.argv[1]
    else:
        print("No command-line arguments provided.")
    
    df_result_tuple = generateDataFrames('resources/data.json') # Initializing the global variables and returning the dataframes

    if df_result_tuple is not None:
        if operation == 'login':
            print("Login operation selected.")
            loginSequence(df_result_tuple)
        elif operation == 'register':
            print("Register operation selected.")
            registerSequence(df_result_tuple)
        else:
            print("Invalid operation type")
            return 1
    else:
        return 1
    
    

def print_data(filePath):
    printdf = pd.read_excel(filePath)
    print(printdf)

if __name__ == '__main__':
    main()

