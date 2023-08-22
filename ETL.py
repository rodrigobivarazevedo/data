import glob                         # this module helps in selecting files 
import pandas as pd                 # this module helps in processing CSV files
import xml.etree.ElementTree as ET  # this module helps in processing XML files.
from datetime import datetime


def extract_from_csv(file_to_process):
    dataframe = pd.read_csv(file_to_process)
    return dataframe


def extract_from_json(file_to_process):
    dataframe = pd.read_json(file_to_process,lines=True)
    return dataframe


def extract_from_xml(file_to_process):
    dataframe = pd.DataFrame(columns=['car_model', 'year_of_manufacture', 'price', 'fuel'])
    tree = ET.parse(file_to_process)
    root = tree.getroot()
    for person in root:
        car_model = person.find("car_model").text
        year_of_manufacture = int(person.find("year_of_manufacture").text)
        price = float(person.find("price").text)
        fuel = person.find("fuel").text
        new_row = {"car_model": car_model, "year_of_manufacture": year_of_manufacture, "price": price, "fuel": fuel}
        dataframe = pd.concat([dataframe, pd.DataFrame([new_row])], ignore_index=True)
    return dataframe

    


tmpfile    = "temp.tmp"               # file used to store all extracted data
logfile    = "logfile.txt"            # all event logs will be stored in this file
targetfile = "transformed_data.csv"   # file where transformed data is stored



def extract():
    extracted_data = pd.DataFrame(columns=['car_model', 'year_of_manufacture', 'price', 'fuel'])  # create an empty data frame to hold extracted data
    
    data = []  # List to hold extracted data from all file types
    
    # Process all csv files
    for csvfile in glob.glob("dealership_data/*.csv"):
        data.append(extract_from_csv(csvfile))
        
    # Process all json files
    for jsonfile in glob.glob("dealership_data/*.json"):
        data.append(extract_from_json(jsonfile))
    
    # Process all xml files
    for xmlfile in glob.glob("dealership_data/*.xml"):
        data.append(extract_from_xml(xmlfile))
    
    # Concatenate all data from different file types
    if data:
        extracted_data = pd.concat(data, ignore_index=True)
        
    return extracted_data




def transfrom(data):
    data["price"] = round(data.price, 2)
    return data

def load(targetfile,data):
    data.to_csv(targetfile)
    


def log(message):
    timestamp_format = '%Y-%h-%d-%H:%M:%S' # Year-Monthname-Day-Hour-Minute-Second
    now = datetime.now() # get current timestamp
    timestamp = now.strftime(timestamp_format)
    with open("logfile.txt","a") as f:
        f.write(timestamp + ',' + message + '\n')


log("ETL Job Started")

log("Extract phase Started")
extracted_data = extract()
log("Extract phase Ended")

log("Transform phase Started")
transformed_data = transfrom(extracted_data)
log("Transform phase Ended")

log("Load phase Started")
load(targetfile,transformed_data)
log("Load phase Ended")

log("ETL Job Ended")
print("ETL Job Ended")