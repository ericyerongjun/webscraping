import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def scrape_Berkeley():
    url = "https://grad.berkeley.edu/admissions/choosing-your-program/list/"
    
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            # Navigate to the URL
            await page.goto(url, wait_until="domcontentloaded")
            
            # Wait for program grid to load
            await page.wait_for_selector("div.program-grid", timeout=15000)
            
            # Scroll to load more content
            for _ in range(3):
                await page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight);")
                await page.wait_for_timeout(2000)
            
            # Get page content
            content = await page.content()
            soup = BeautifulSoup(content, "html.parser")
            
            # Find all program-grid elements
            programs = soup.find_all("div", class_="program-grid")
            print(f"Found {len(programs)} program-grid elements")
            
            titles = []
            for program in programs:
                # Find the <a> tag within the nested structure
                a_tag = program.select_one("div.program-grid--title div a")
                if a_tag:
                    # Extract the text from the <p> tag inside the <a> tag
                    p_tag = a_tag.find("p")
                    if p_tag:
                        title = p_tag.text.strip()
                        titles.append(title)
                    else:
                        print("No <p> tag found inside <a>:", a_tag)
                else:
                    print("No <a> tag found in program:", program)
            
            # Print titles
            for t in titles:
                print(t)
            
            # If no titles found, print the soup for debugging
            if not titles:
                print("No titles found. HTML content:")
                print(soup.prettify())
                
        except Exception as e:
            print(f"Error during scraping: {str(e)}")
            
        finally:
            # Close browser
            await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_Berkeley())