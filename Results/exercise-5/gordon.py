## Script to fetch today's lunch menu from the UTB Nord website
#  and update index.html with the new date and lunch information.

# Importing necessary libraries
import requests
from bs4 import BeautifulSoup


# Define the UTB Nord website URL
url = "https://www.utbnord.se/"

# Get todays lunch
def get_lunch(webresponse):
    soup = BeautifulSoup(webresponse.text, "html.parser")
    lunch = soup.find_all("div", class_="lunch-wrapper__wrap")[0].text.split()
    return " ".join(lunch[3:])

# Get todays date
def get_date(webresponse):
    soup = BeautifulSoup(webresponse.text, "html.parser")
    lunch = soup.find_all("div", class_="lunch-wrapper__wrap")[0].text.split()
    return " ".join(lunch[:3])

try:
    # Fetch the webpage
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(
            f"Error loading webpage, status code: {response.status_code}"
            )

    # Extract lunch and date information
    lunch = get_lunch(response)
    date = get_date(response)

    # Read the existing index.html file, update it with the new date and lunch information
    with open("index.html", "r") as file:
        old_index = file.read()

        soup = BeautifulSoup(old_index, "html.parser")
        old_date = soup.find_all("p", class_="date")[0].text
        old_lunch = soup.find_all("p", class_="food")[0].text

        new_index = old_index.replace(old_date, date)
        new_index = new_index.replace(old_lunch, lunch)

### BUG: If webpage fecth fails, this will write an empty index.html file.
###      Error handling should be added to prevent this.
    with open("index.html", "w") as file:
        file.write(new_index)

# Error handling
except Exception as e:
    print(f"Error: {str(e)}")