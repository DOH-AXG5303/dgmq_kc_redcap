import pandas as pd
import os, re
from datetime import datetime, timedelta

def scan_directory(path_input = None):
    """
    Query present working directory for all .csv files and all .xlsx files

    args:
        path_input = string, path to directory to be scanned. 
    return: list of file names
    """
    if path_input is None:
        path = "./"
        
    path = path_input 
    files = []
    
    # iterate filenames in directory and append .xlsx to files list
    for fname in os.listdir(path):
        if re.search(r'.csv', fname):
            files.append(fname)
        if re.search(r'.xlsx', fname):
            files.append(fname)
        else:
            pass
        
    return files

def check_csv_files(files):
    """
    verify rules in the input list of strings (file names):
        1)pwd contains exactly 1 .csv file
        2)pwd contains exactly 1 Records file
        
    args:
        files: list of strings
    return: bool
    """
    # rules for files: exactly 1 xlsx file and exactly 1 file names "Records.xlsx"
    xls_files = 0
    csv_files = 0
    for i in files:
        if i.endswith(".csv"):
            csv_files += 1
        if i == ("Records.xlsx"):
            xls_files += 1

    rules = [xls_files==1, csv_files==1]

    # verify all rules to be True
    if all(rules):
        print("Conditions are met. Present directory contains one .csv file and one Records.xlsx file")
        return all(rules)

    else:
        raise Exception("Condition not met: Exactly one .csv file and one Records.xlsx file is expected in directory")

def load_files(files, condition):
    """
    import .csv and Records.xlsx files in the files list argument

    args:
        files: list of strings
        condition = bool, output from check conditions function
 
    return: dict of dataframes
    """
    path = "./"  # path to pwd
    df_dict = {} 
    
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
    
    # import excel into dataframes if file condition has been met
    if condition:
        for i in files:
            if i == "Records.xlsx":  # laod instructions for Records.xlsx file
                df_dict["Records"] = pd.read_excel((path + i),
                                                   sheet_name="Master",
                                                   engine="openpyxl")
            
            else:
                df_dict["Travel"] = pd.read_csv(path + files[0], parse_dates = date_clms)
    else:
        print("FAILED TO MEET CONDITION: Excel files were not imported")
        raise Exception("Condition not met: Exactly one .csv file and one Records.xlsx file is expected in directory")
    return df_dict

def import_data():
    files = scan_directory()
    condition = check_csv_files(files)
    df_dict = load_files(files, condition)
    
    return df_dict


def infectious_check(df):
    """
    Keep the rows of data where ANY of the departure dates fall between -2 days before test to +10 days after test
    
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

    days10 = timedelta(days=10)
    days2 = timedelta(days = 2)

    #True for all departures that occur before (test collection + 10days)
    cond_1 = df[date_departure].lt((df['Test collection date']+days10), axis = 0)

    #True for all departures that occue after (test collection - 2days)
    cond_2 = df[date_departure].gt((df['Test collection date']-days2), axis = 0)

    # combined conditions, ANY departures that fall between -2days before test, and +10 days after test 
    df = df[(cond_1 & cond_2).any(axis=1)].copy()
    
    return df

if (__name__=="__main__"):

    df_dict = import_data()
    
    df_travel = infectious_check(df_dict["Travel"])
    
    df_travel.to_csv("./Redcap_Result.csv", index=False)