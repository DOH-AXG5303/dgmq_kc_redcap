import pandas as pd
import os, re
from datetime import datetime, timedelta

def scan_directory():
    """
    Query present working directory for all .csv files

    return: list of .csv file names
    """
    path = "./"  # path to pwd
    files = []

    # iterate filenames in directory and append .xlsx to files list
    for fname in os.listdir(path):
        if re.search(r'.csv', fname):
            files.append(fname)
        else:
            pass
        
    return files


def check_csv_files(files):
    """
    verify rules in the input list of strings (file names):
        1)pwd contains exactly 1 .csv file
        
    args:
        files: list of strings
    return: bool
    """

    # rules for files: exactly 2 files, Records.xlxs is present
    rules = [len(files) == 1]

    # verify all rules to be True
    if all(rules):
        print("Conditions is met. Present directory contains 1 .csv file")
        return all(rules)

    else:
        raise Exception("Condition not met: Exactly 1 .csv file is expected in directory")


def load_csv_files(files):
    """
    import .csv file in the files list argument

    args:
        files: list of string
 
    return: dict of dataframes
    """
    path = "./"  # path to pwd
    
    #list of columns that should be datetime type
    date_clms = [
    'Test collection date',
    'Date of departure',
    'Date of departure.1',
    'Date of departure.2',   
    'Date of departure.3',
    'Date of departure.4',
    'Date of departure.5',
    'Date of departure.6',]
    
    df = pd.read_csv(path + files[0], parse_dates = date_clms)

    return df

def filter_by_travel_date(df):
    """
    Keep the rows of data that meet the rule:
        - any of the multiple departure dates fall within the range: 14 days before collection date, to collection date. 
        
    args:
        df: panadas Dataframe
    return:
        df: pandas Dataframe
    """

    date_departure = [
        'Date of departure',
        'Date of departure.1',
        'Date of departure.2',   
        'Date of departure.3',
        'Date of departure.4',
        'Date of departure.5',
        'Date of departure.6',]

    days14 = timedelta(days=14)

    #departures that occur before the test date
    cond_1 = df[date_departure].lt((df['Test collection date']), axis = 0)

    #departures that occur after (test date minus 14 days)
    cond_2 = df[date_departure].gt((df['Test collection date']-days14), axis = 0)

    # combined conditions, ANY departures that fall into the 14 days window prior to test date
    df = df[(cond_1 & cond_2).any(axis=1)].copy()
    
    return df

if (__name__=="__main__"):

    files = scan_directory()
    check_csv_files(files)
    df = load_csv_files(files)
    df = filter_by_travel_date(df)

    df.to_csv("./Redcap_Result.csv", index=False)