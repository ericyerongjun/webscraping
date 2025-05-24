from playwright.sync_api import sync_playwright, Playwright
from bs4 import BeautifulSoup

def scrape_hktvmall():
    url = "https://www.hktvmall.com/hktv/en/search_a?keyword=iphone"
    
    with sync_playwright() as p:
        # Launch browser in headless mode
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # Load the page
            page.goto(url)
            
            # Wait for dynamic content (try product-brief-wrapper or info-wrapper)
            try:
                page.wait_for_selector("span.product-brief-wrapper", timeout=10000)
            except:
                print("No 'product-brief-wrapper' found. Trying 'info-wrapper'...")
                page.wait_for_selector("div.info-wrapper", timeout=10000)
            
            # Get page content
            soup = BeautifulSoup(page.content(), "html.parser")
            
            # Try finding product-brief-wrapper as in your code
            product_brief_wrapper = soup.find_all("span", class_="product-brief-wrapper")
            
            if product_brief_wrapper:
                for product in product_brief_wrapper:
                    info_wrapper = product.find("div", class_="info-wrapper")
                    if not info_wrapper:
                        print("No 'info-wrapper' found in this product-brief-wrapper.")
                        continue
                    upper_wrapper = info_wrapper.find("div", class_="upper-wrapper")
                    if not upper_wrapper:
                        print("No 'upper-wrapper' found in this info-wrapper.")
                        continue
                    product_name = upper_wrapper.find("div", class_="brand-product-name")
                    if product_name:
                        print(product_name.text.strip())
                    else:
                        print("No 'brand-product-name' found in this upper-wrapper.")
            else:
                # Fallback: try info-wrapper directly
                print("No 'product-brief-wrapper' found. Checking 'info-wrapper' directly...")
                info_wrapper = soup.find_all("div", class_="info-wrapper")
                if not info_wrapper:
                    print("No elements found with class 'info-wrapper'. Check class names or page structure.")
                else:
                    for info in info_wrapper:
                        upper_wrapper = info.find("div", class_="upper-wrapper")
                        if not upper_wrapper:
                            # Try brand-product-name directly in info-wrapper
                            product_name = info.find("div", class_="brand-product-name")
                            if product_name:
                                print(product_name.text.strip())
                            else:
                                print("No 'brand-product-name' or 'upper-wrapper' found in this info-wrapper.")
                            continue
                        product_name = upper_wrapper.find("div", class_="brand-product-name")
                        if product_name:
                            print(product_name.text.strip())
                        else:
                            print("No 'brand-product-name' found in this upper-wrapper.")
        
        except Exception as e:
            print(f"Error during scraping: {e}")
        finally:
            # Close browser
            browser.close()

if __name__ == "__main__":
    scrape_hktvmall()