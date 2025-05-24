from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

try:
    service = webdriver.Chrome(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
except Exception as e:
    exit()
    

url = "https://www.hktvmall.com/hktv/en/search_a?keyword=iphone"
try:
    driver.get(url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "info-wrapper"))
    )
except Exception as e:
    driver.quit()
    exit()

soup = BeautifulSoup(driver.page_source, 'html.parser')

peoduct_brief_wrapper = soup.find_all("span", class_= "product-brief-wrapper")

for product in peoduct_brief_wrapper:
    info_wrapper = product.find("div", class_="info-wrapper")
    upper_wrapper = info_wrapper.find("div", class_="upper-wrapper")
    product_name = upper_wrapper.find("div", class_="brand-product-name").text.strip()
    print(product_name)
    
driver.quit()
    
