import requests
from bs4 import BeautifulSoup

# 1. Download the page
url = "https://www.marvel.com/movies"
response = requests.get(url)

# 2. Parse the HTML
soup = BeautifulSoup(response.text, "html.parser")

# 3. Find and print the title tag
print(soup.title.text)