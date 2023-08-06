import requests
from bs4 import BeautifulSoup

def get():
    # Requests data from page
    page = requests.get("https://iplocation.com/")
    soup = BeautifulSoup(page.content, 'html.parser')

    ip = soup.find("b", {"class": "ip"}).text

    return ip