import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def scrape_Bloomberg_Originals():
    url = "https://www.youtube.com/@business/videos"
    
    async with async_playwright() as p:
        # Launch browser (headless=False for debugging, True for production)
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        try:
            # Navigate to the URL
            await page.goto(url, wait_until="domcontentloaded")
            
            # Wait for video titles to load
            await page.wait_for_selector("a#video-title-link", timeout=15000)
            
            # Scroll to load more videos (optional, adjust as needed)
            for _ in range(3):  # Scroll 3 times to load more content
                await page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight);")
                await page.wait_for_timeout(2000)  # Wait for content to load
            
            # Get page content
            content = await page.content()
            soup = BeautifulSoup(content, "html.parser")
            
            # Find video titles (using the <a> tag with id="video-title-link")
            titles = soup.find_all("a", id="video-title-link")
            
            if titles:
                print(f"Found {len(titles)} video titles:")
                for i, title in enumerate(titles, 1):
                    title_text = title.get("title") or title.text.strip()
                    if title_text:
                        print(f"{i}. {title_text}")
                    else:
                        print(f"{i}. [Empty or inaccessible title]")
            else:
                print("No video titles found.")
                
        except Exception as e:
            print(f"Error during scraping: {str(e)}")
            
        finally:
            # Close browser
            await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_Bloomberg_Originals())