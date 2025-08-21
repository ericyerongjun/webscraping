from playwright.async_api import async_playwright, Playwright
from bs4 import BeautifulSoup
import asyncio

async def scrape_Bloomberg_Latest():
    url = "https://www.bloomberg.com/latest?utm_source=homepage&utm_medium=web&utm_campaign=latest"
    
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            print("Loading Bloomberg Latest page...")
            await page.goto(url, wait_until='networkidle')
            
            # Wait a bit for dynamic content to load
            await page.wait_for_timeout(3000)
            
            print("Page loaded, looking for content...")
            
            # Try multiple possible selectors
            selectors_to_try = [
                "div.Latest_storyPadding__GBJUE",
                "[class*='Latest_storyPadding']",
                "[class*='storyPadding']",
                "article",
                "[data-component='story']",
                ".story"
            ]
            
            found_selector = None
            for selector in selectors_to_try:
                try:
                    await page.wait_for_selector(selector, timeout=5000)
                    found_selector = selector
                    print(f"Found content with selector: {selector}")
                    break
                except:
                    continue
            
            if not found_selector:
                print("Could not find expected selectors. Let's check what's actually on the page...")
                # Get page content and look for any story-related elements
                content = await page.content()
                soup = BeautifulSoup(content, "html.parser")
                
                # Print some debug information
                print("Page title:", await page.title())
                print("Looking for any elements with 'story' or 'latest' in class names...")
                
                story_elements = soup.find_all(attrs={"class": lambda x: x and any(word in str(x).lower() for word in ['story', 'latest', 'article', 'headline'])})
                print(f"Found {len(story_elements)} potential story elements")
                
                if story_elements:
                    for i, elem in enumerate(story_elements[:3]):
                        print(f"Element {i+1}: {elem.name} with class {elem.get('class')}")
                
                return
        
            # Scroll to load more content
            print("Scrolling to load more content...")
            for i in range(3):
                await page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight);")
                await page.wait_for_timeout(2000)
                print(f"Scroll {i+1}/3 completed")
          
            # Get page content and parse with BeautifulSoup
            content = await page.content()
            soup = BeautifulSoup(content, "html.parser")
            
            # Use the selector that worked
            if found_selector == "div.Latest_storyPadding__GBJUE":
                latest_stories = soup.find_all("div", class_="Latest_storyPadding__GBJUE")
            else:
                latest_stories = soup.select(found_selector)
        
            print(f"Found {len(latest_stories)} stories")
            
            if not latest_stories:
                print("No stories found with the expected structure. Trying alternative extraction...")
                # Try to find any headlines or articles
                headlines = soup.find_all(attrs={"class": lambda x: x and 'headline' in str(x).lower()})
                if headlines:
                    print(f"Found {len(headlines)} headlines using alternative method")
                    for i, headline in enumerate(headlines[:10]):
                        title = headline.get_text().strip()
                        if title:
                            print(f"{i+1}. {title}")
                return
        
            titles = []
            times = []
        
            for story in latest_stories:
                try:
                    # Extract title using the correct selector
                    title_element = story.select_one("div.Latest_itemTextContainer__YMnVV a div span")
                    if title_element:
                        title = title_element.get_text().strip()
                        titles.append(title)
                    
                    # Extract time using the correct selector
                    time_element = story.select_one("div.Latest_desktopTimestamp__oiCLC div.Latest_itemTimestamp__SqjF_ time")
                    if time_element:
                        time = time_element.get_text().strip()
                        times.append(time)
                except Exception as e:
                    print(f"Error extracting data from story: {e}")
                    continue
            
            # Print results
            for i, (title, time) in enumerate(zip(titles, times)):
                print(f"{i+1}. Title: {title}")
                print(f"   Time: {time}")
                print("-" * 80)
                
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_Bloomberg_Latest())