#!mamba install pandas==1.3.3 -y
#!mamba install requests==2.26.0 -y
#!mamba install bs4==4.10.0 -y
#!mamba install html5lib==1.1 -y


from bs4 import BeautifulSoup
import html5lib
import requests
import pandas as pd

from bs4 import BeautifulSoup
import requests
import pandas as pd

# URL of the webpage
url = "https://web.archive.org/web/20200318083015/https://en.wikipedia.org/wiki/List_of_largest_banks"

# Send a GET request to the URL to fetch the HTML content
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Assign the HTML content to the variable html_data
    html_data = response.text
else:
    print("Failed to retrieve webpage content.")

# Parse the HTML content using BeautifulSoup and html5lib
soup = BeautifulSoup(html_data, "html5lib")

# Find the <h2> element with the id "By_market_capitalization"
headline_element = soup.find("span", class_="mw-headline", id="By_market_capitalization")

# Find the table element that follows the headline
table = headline_element.find_next("table")

if table:
    data = pd.DataFrame(columns=["Name", "Market Cap (US$ Billion)"])
   
    # Loop through table rows
    for row in table.find_all("tr")[1:]:  # skip header
        columns = row.find_all("td")
        if len(columns) >= 2:
            bank_name = columns[1].get_text(strip=True)
            market_cap = columns[2].get_text(strip=True)
            new_row = {"Name": bank_name, "Market Cap (US$ Billion)": market_cap}
            data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
        
    # Display the first five rows using head
    print(data.head())

    # Save DataFrame to JSON
    data.to_json("bank_market_cap.json", orient="records", indent=4)

else:
    print("Failed to find the 'By market capitalization' table.")
