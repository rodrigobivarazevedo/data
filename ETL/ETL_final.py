import glob
import pandas as pd
from datetime import datetime


def extract_from_json(file_to_process):
    dataframe = pd.read_json(file_to_process)
    return dataframe

def extract_from_csv(file_path):
    # Load the CSV file and return a DataFrame
    df = pd.read_csv(file_path, index_col=0)
    return df
    
def extract_bank():
    df_bank_market_cap = pd.DataFrame(columns=['Name','Market Cap (US$ Billion)'])
    data_bank = []  # List to hold extracted data from all file types
        
    # Process all json files
    for jsonfile in glob.glob("ETL/WEB_scraping/*.json"):
        data_bank.append(extract_from_json(jsonfile))

    if data_bank:
        df_bank_market_cap = pd.concat(data_bank, ignore_index=True)
        return df_bank_market_cap


def extract_csv():
    # Write your code here
    df_exchange_rates = pd.DataFrame(columns=['Rates'])
    data_rates = []  # List to hold extracted data from all file types
        
    # Process all CSV files
    for csvfile in glob.glob("ETL/API/*.csv"):
        data_rates.append(extract_from_csv(csvfile))

    if data_rates:
        df_exchange_rates = pd.concat(data_rates, axis=1, ignore_index=False)
        # Find the exchange rate for British pounds (GBP)
        exchange_rate_GBP = df_exchange_rates.loc["GBP", "Rate"]
        return exchange_rate_GBP, df_exchange_rates



def transform(exchange_rate, bank_caps):
    
    # Convert the "Market Cap (US$ Billion)" column to GBP
    bank_caps["Market Cap (GBP$ Billion)"] = bank_caps["Market Cap (US$ Billion)"] * exchange_rate
    # Round the "Market Cap (GBP$ Billion)" column to 3 decimal places
    bank_caps["Market Cap (GBP$ Billion)"] = bank_caps["Market Cap (GBP$ Billion)"].round(3)
    # Drop the original "Market Cap (US$ Billion)" column
    bank_caps.drop("Market Cap (US$ Billion)", axis=1, inplace=True)
    return bank_caps


def load(data):
    data.to_csv("bank_market_cap_gbp.csv", index=False)
    print("DataFrame saved to bank_market_cap_gbp.csv")


logfile  = "logfile.txt"            # all event logs will be stored in this file

def log(message):
    timestamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second
    now = datetime.now() # get current timestamp
    timestamp = now.strftime(timestamp_format)
    with open("logfile.txt","a") as f:
        f.write(timestamp + ',' + message + '\n')


log("ETL Job Started")

log("Extract phase Started")
exchange_rate, _ = extract_csv()
df_bank_caps = extract_bank()
log("Extract phase Ended")

log("Transform phase Started")
transformed_df = transform(exchange_rate, df_bank_caps)
log("Transform phase Ended")

log("Load phase Started")
load(transformed_df)
log("Load phase Ended")

log("ETL Job Ended")
print("ETL Job Ended")