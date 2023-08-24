import requests
import pandas as pd


# Write your code here
url = "http://api.exchangeratesapi.io/v1/latest?base=EUR&access_key=b0658ea7ffcca0400f78d747171783f6"  #Make sure to change ******* to your API key.

# Send a GET request to the URL to fetch the HTML content
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Load the API data into a JSON format
    api_data = response.json()
else:
    print("Failed to retrieve api data.")



# Turn the data into a dataframe
# Extract the rates dictionary from the JSON
rates = api_data.get("rates", {})    #  The get() method is used to extract the value associated with the key "rates" from the api_data dictionary. If the "rates" key is not found in the dictionary, the second argument (an empty dictionary {}) is returned as the default value. This helps prevent errors if the "rates" key is missing in the API response

# Create a DataFrame from the rates dictionary
df = pd.DataFrame.from_dict(rates, orient="index", columns=["Rate"])

print(df.head())

# Save the DataFrame as a CSV file
df.to_csv("exchange_rates_1.csv")