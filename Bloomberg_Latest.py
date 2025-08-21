from playwright.async_api import async_playwright, Playwright
from bs4 import BeautifulSoup
import asyncio

async def scrape_Bloomberg_Latest():
    url = "https://www.bloomberg.com/latest"
    
    async with async_playwright() as p:
        # Launch browser with more human-like settings
        browser = await p.chromium.launch(
            headless=False,  # Set to True if you don't want to see the browser
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor'
            ]
        )
        
        # Create context with human-like settings
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        )
        
        page = await context.new_page()
        
        # Add stealth settings
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined,
            });
        """)
        
        try:
            print("Loading Bloomberg Latest page...")
            # Use a more lenient wait condition and longer timeout
            await page.goto(url, wait_until='domcontentloaded', timeout=60000)
            
            # Check if we hit a bot detection page
            page_title = await page.title()
            print(f"Page title: {page_title}")
            
            if "robot" in page_title.lower() or "captcha" in page_title.lower():
                print("⚠️  Bot detection detected!")
                print("Bloomberg is blocking automated access.")
                print("Waiting 30 seconds for manual intervention (solve CAPTCHA if visible)...")
                await page.wait_for_timeout(30000)
                
                # Check again after waiting
                page_title = await page.title()
                if "robot" in page_title.lower():
                    print("Still on bot detection page. Exiting...")
                    return
            
            # Handle cookie consent or terms acceptance
            print("Looking for accept/consent buttons...")
            
            # Common selectors for accept buttons
            accept_selectors = [
                'button[data-testid="accept-all"]',
                'button[id*="accept"]',
                'button[class*="accept"]',
                'button:has-text("Accept")',
                'button:has-text("Accept All")',
                'button:has-text("I Accept")',
                'button:has-text("Continue")',
                'button:has-text("Agree")',
                '[data-testid="cookie-accept"]',
                '.cookie-accept',
                '#cookie-accept'
            ]
            
            accepted = False
            for selector in accept_selectors:
                try:
                    element = await page.wait_for_selector(selector, timeout=3000)
                    if element:
                        print(f"Found accept button with selector: {selector}")
                        await element.click()
                        print("Clicked accept button")
                        await page.wait_for_timeout(2000)
                        accepted = True
                        break
                except Exception:
                    continue
            
            if not accepted:
                print("No accept button found, or already accepted. Continuing...")
            
            # Wait for page to fully load after acceptance
            await page.wait_for_timeout(5000)
            
            print("Looking for content...")
            
            # Try multiple possible selectors
            selectors_to_try = [
                "div.Latest_storyPadding__GBJUE",
                "[class*='Latest_storyPadding']",
                "[class*='storyPadding']",
                "article",
                "[data-component='story']",
                ".story",
                "[class*='story']",
                "[class*='article']"
            ]
            
            found_selector = None
            for selector in selectors_to_try:
                try:
                    await page.wait_for_selector(selector, timeout=5000)
                    found_selector = selector
                    print(f"Found content with selector: {selector}")
                    break
                except Exception:
                    continue
            
            if not found_selector:
                print("Could not find expected selectors. Let's check what's actually on the page...")
                # Get page content and look for any story-related elements
                content = await page.content()
                soup = BeautifulSoup(content, "html.parser")
                
                # Print some debug information
                current_title = await page.title()
                print("Current page title:", current_title)
                print("Looking for any elements with 'story' or 'latest' in class names...")
                
                story_elements = soup.find_all(attrs={"class": lambda x: x and any(word in str(x).lower() for word in ['story', 'latest', 'article', 'headline'])})
                print(f"Found {len(story_elements)} potential story elements")
                
                if story_elements:
                    for i, elem in enumerate(story_elements[:5]):
                        print(f"Element {i+1}: {elem.name} with class {elem.get('class')}")
                        text = elem.get_text().strip()[:100]  # First 100 chars
                        if text:
                            print(f"   Text: {text}")
                
                # Try alternative extraction
                headlines = soup.find_all(attrs={"class": lambda x: x and 'headline' in str(x).lower()})
                if headlines:
                    print(f"\nFound {len(headlines)} headlines using alternative method:")
                    for i, headline in enumerate(headlines[:10]):
                        title = headline.get_text().strip()
                        if title:
                            print(f"{i+1}. {title}")
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
                print("No stories found with the expected structure.")
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
            print(f"\n=== Found {len(titles)} articles ===")
            for i, (title, time) in enumerate(zip(titles, times)):
                print(f"{i+1}. Title: {title}")
                print(f"   Time: {time}")
                print("-" * 80)
                
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            await context.close()
            await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_Bloomberg_Latest())
        
        
        