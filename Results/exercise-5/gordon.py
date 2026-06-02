# Importing necessary libraries
import requests
from bs4 import BeautifulSoup

# I am looking for:
"""
<div class="lunch-wrapper"><h4> Dagens lunch i Övertorneå </h4>
    <div class="lunch-wrapper__wrap">
        <p>
            " Tis. 02. 06 "
            <br><strong>Gulaschgryta med kokt potatis</strong>
        </p>
    </div>
    <a class="btn btn-primary" href="/sv/skolan/restaurang/a-la-carte-meny">
        Till A la Carte Restaurangen
    </a>
    <a class="btn btn-primary" href="/sv/skolan/restaurang/lunchmeny-i-hedenaset">
        Till Lunchmeny i Hedenäset
    </a>
</div>
"""


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

    lunch = get_lunch(response)
    date = get_date(response)

    with open("index.html", "r") as file:
        old_index = file.read()

        soup = BeautifulSoup(old_index, "html.parser")
        old_date = soup.find_all("p", class_="date")[0].text
        old_lunch = soup.find_all("p", class_="food")[0].text

        new_index = old_index.replace(old_date, date)
        new_index = new_index.replace(old_lunch, lunch)

    with open("index.html", "w") as file:
        file.write(new_index)

except Exception as e:
    print(f"Error: {str(e)}")


# Put the information in a index.html file