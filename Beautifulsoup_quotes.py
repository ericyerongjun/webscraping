import requests
from bs4 import BeautifulSoup

# URL of the website to scrape
url = "http://quotes.toscrape.com"

# Send a GET request to fetch the webpage
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the webpage content with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all quote elements
    quotes = soup.find_all('div', class_='quote')
    
    # Extract and print quote text and author
    for quote in quotes:
        text = quote.find('span', class_='text').text
        author = quote.find('small', class_='author').text
        print(f"Quote: {text}")
        print(f"Author: {author}")
        print("-" * 50)
else:
    print(f"Failed to retrieve webpage. Status code: {response.status_code}")