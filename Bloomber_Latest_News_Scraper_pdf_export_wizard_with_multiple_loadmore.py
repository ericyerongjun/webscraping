from playwright.async_api import async_playwright, Playwright
from bs4 import BeautifulSoup
import asyncio
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime
from fake_useragent import UserAgent

def create_pdf_report(titles, times, filename="bloomberg_latest_news.pdf"):
    """Create a PDF report with the scraped Bloomberg news"""
    print(f"Creating PDF report: {filename}")
    
    # Create the PDF document
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []
    
    # Title style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    # Article title style
    article_title_style = ParagraphStyle(
        'ArticleTitle',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=6,
        textColor='darkblue'
    )
    
    # Time style
    time_style = ParagraphStyle(
        'TimeStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor='gray',
        spaceAfter=12
    )
    
    # Add title
    title = Paragraph("Bloomberg Latest News Report", title_style)
    story.append(title)
    
    # Add generation timestamp
    timestamp = Paragraph(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal'])
    story.append(timestamp)
    story.append(Spacer(1, 0.2*inch))
    
    # Add articles
    for i, (title_text, time_text) in enumerate(zip(titles, times), 1):
        # Article number and title
        article_title = Paragraph(f"{i}. {title_text}", article_title_style)
        story.append(article_title)
        
        # Article time
        article_time = Paragraph(f"Published: {time_text}", time_style)
        story.append(article_time)
        
        # Add some space between articles
        story.append(Spacer(1, 0.1*inch))
    
    # Build PDF
    doc.build(story)
    print(f"PDF report saved as: {filename}")

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
            user_agent=UserAgent().chrome
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
            
            # Scroll to load more content and click "Load More" buttons
            print("Scrolling and looking for 'Load More' buttons...")
            
            load_more_clicked = 0
            max_load_more_attempts = 5  # Maximum number of times to click "Load More"
            
            for scroll_attempt in range(6):  # Increased scroll attempts
                # Scroll down first
                await page.evaluate("window.scrollTo(0, document.documentElement.scrollHeight);")
                await page.wait_for_timeout(2000)
                print(f"Scroll {scroll_attempt+1}/6 completed")
                
                # Look for "Load More" button with various possible selectors
                load_more_selectors = [
                    'button:has-text("Load More")',
                    'button:has-text("Show More")',
                    'button:has-text("More Stories")',
                    'button:has-text("View More")',
                    '[data-testid="load-more"]',
                    '[class*="load-more" i]',
                    '[class*="LoadMore" i]',
                    '[class*="show-more" i]',
                    'button[aria-label*="load more" i]',
                    'button[aria-label*="show more" i]',
                    '.load-more-button',
                    '#load-more',
                    'button[class*="More"]'
                ]
                
                load_more_found = False
                for selector in load_more_selectors:
                    try:
                        # Wait a short time for the button to appear
                        load_more_button = await page.wait_for_selector(selector, timeout=2000)
                        if load_more_button:
                            # Check if button is visible and clickable
                            is_visible = await load_more_button.is_visible()
                            is_enabled = await load_more_button.is_enabled()
                            
                            if is_visible and is_enabled and load_more_clicked < max_load_more_attempts:
                                print(f"Found 'Load More' button with selector: {selector}")
                                
                                # Scroll the button into view
                                await load_more_button.scroll_into_view_if_needed()
                                await page.wait_for_timeout(1000)
                                
                                # Click the button
                                await load_more_button.click()
                                load_more_clicked += 1
                                load_more_found = True
                                print(f"Clicked 'Load More' button #{load_more_clicked}")
                                
                                # Wait for new content to load
                                await page.wait_for_timeout(3000)
                                break
                    except Exception as e:
                        continue
                
                # If we found and clicked a load more button, continue scrolling and looking
                if not load_more_found:
                    # No load more button found in this scroll, continue to next scroll
                    continue
            
            print(f"Finished scrolling. Clicked 'Load More' {load_more_clicked} times.")
            
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
            
            # Create PDF report
            if titles and times:
                create_pdf_report(titles, times)
            else:
                print("No data to export to PDF")
                
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            await context.close()
            await browser.close()

if __name__ == "__main__":
    asyncio.run(scrape_Bloomberg_Latest())