from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import csv

def scrape_yf():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        url = "https://finance.yahoo.com/markets/crypto/all/"
        page.goto(url)
        page.wait_for_selector("table")
        
        html = page.content()
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find("table")
        if table:
            rows = table.find_all("tr")
            data = []
            for row in rows:
                cols = [col.get_text(strip=True) for col in row.find_all(["td", "th"])]
                data.append(cols)
            # Write to CSV
            with open("crypto_data.csv", "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(data)
            print("CSV file 'crypto_data.csv' has been created.")
        else:
            print("No table found.")
        
        browser.close()

if __name__ == "__main__":
    scrape_yf()