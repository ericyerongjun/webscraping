# Web Scraping Projects Collection

This repository contains a collection of web scraping projects demonstrating various techniques and tools for extracting data from different websites. The projects showcase the use of multiple Python libraries and frameworks for web scraping, including Playwright, Selenium, BeautifulSoup, and more.

## Prerequisites

Before running any of the projects in this repository, you need to ensure that your system has the following prerequisites installed:

### Python Requirements

- **Python 3.7+** (Python 3.8+ recommended)
- **pip** (Python package installer)

### Required Python Packages

The projects in this repository require several Python packages. Install them using pip:

```bash
pip install playwright
pip install beautifulsoup4
pip install selenium
pip install webdriver-manager
pip install reportlab
pip install fake-useragent
pip install requests
```

#### Alternative: Install All Dependencies at Once

You can create a `requirements.txt` file and install all dependencies at once:

```bash
# Create requirements.txt file
cat > requirements.txt << EOF
playwright>=1.40.0
beautifulsoup4>=4.12.0
selenium>=4.15.0
webdriver-manager>=4.0.0
reportlab>=4.0.0
fake-useragent>=1.4.0
requests>=2.31.0
EOF

# Install all dependencies
pip install -r requirements.txt
```

### Browser Setup for Playwright

After installing Playwright, you need to install the browser binaries:

```bash
# Install Playwright browsers (Chrome, Firefox, Safari)
playwright install

# Or install specific browsers only
playwright install chromium
playwright install firefox
```

### Chrome Driver Setup for Selenium

The Selenium scripts use `webdriver-manager` which automatically downloads and manages ChromeDriver. However, you need to have Google Chrome installed on your system:

- **Windows**: Download from [Google Chrome website](https://www.google.com/chrome/)
- **macOS**: Download from [Google Chrome website](https://www.google.com/chrome/) or use Homebrew: `brew install --cask google-chrome`
- **Linux**: Use your distribution's package manager:
  ```bash
  # Ubuntu/Debian
  sudo apt-get install google-chrome-stable
  
  # CentOS/RHEL/Fedora
  sudo dnf install google-chrome-stable
  ```

## Quick Setup Verification

This repository includes a test script (`test_setup.py`) to verify that all dependencies are installed correctly:

```bash
python3 test_setup.py
```

The script will:
- Check if all required Python packages are importable
- Provide clear feedback on what's working and what needs attention
- Give you next steps based on the results

## Projects Overview

### 1. **BeautifulSoup Quotes Scraper** (`Beautifulsoup_quotes.py`)
- **Description**: Simple web scraper that extracts quotes from quotes.toscrape.com
- **Dependencies**: `requests`, `beautifulsoup4`
- **Usage**: `python3 Beautifulsoup_quotes.py`

### 2. **Berkeley PhD Programs Scraper** (`Berkeley_PhD.py`)
- **Description**: Scrapes PhD program listings from UC Berkeley's graduate admissions website
- **Dependencies**: `playwright`, `beautifulsoup4`, `asyncio`
- **Usage**: `python3 Berkeley_PhD.py`

### 3. **Bloomberg News Scrapers**
Multiple Bloomberg scrapers with different approaches:

#### 3.1 **Bloomberg Latest News** (`Bloomberg_Latest.py`)
- **Description**: Scrapes latest news from Bloomberg with bot detection handling
- **Dependencies**: `playwright`, `beautifulsoup4`, `fake-useragent`, `asyncio`
- **Features**: Bot detection bypass, cookie consent handling
- **Usage**: `python3 Bloomberg_Latest.py`

#### 3.2 **Bloomberg News PDF Exporter** (`Bloomberg_Latest_News_pdf_exporter.py`)
- **Description**: Scrapes Bloomberg news and exports to PDF format
- **Dependencies**: `playwright`, `beautifulsoup4`, `reportlab`, `fake-useragent`, `asyncio`
- **Output**: Creates `bloomberg_latest_news.pdf`
- **Usage**: `python3 Bloomberg_Latest_News_pdf_exporter.py`

#### 3.3 **Bloomberg Advanced Scraper** (`Bloomber_Latest_News_Scraper_pdf_export_wizard_with_multiple_loadmore.py`)
- **Description**: Advanced Bloomberg scraper with multiple "Load More" button handling and PDF export
- **Dependencies**: `playwright`, `beautifulsoup4`, `reportlab`, `fake-useragent`, `asyncio`
- **Features**: Dynamic content loading, PDF generation
- **Usage**: `python3 Bloomber_Latest_News_Scraper_pdf_export_wizard_with_multiple_loadmore.py`

#### 3.4 **Bloomberg Originals YouTube** (`Bloomberg_Originals.py`)
- **Description**: Scrapes Bloomberg YouTube channel for video titles
- **Dependencies**: `playwright`, `beautifulsoup4`, `asyncio`
- **Usage**: `python3 Bloomberg_Originals.py`

### 4. **Cryptocurrency Data Scraper** (`Crypto_yf.py`)
- **Description**: Scrapes cryptocurrency data from Yahoo Finance and exports to CSV
- **Dependencies**: `playwright`, `beautifulsoup4`, `csv`
- **Output**: Creates `crypto_data.csv`
- **Usage**: `python3 Crypto_yf.py`

### 5. **HKTVmall Product Scrapers**
Two different approaches for scraping HKTVmall:

#### 5.1 **Selenium Version** (`Selenium_hktvmall.py`)
- **Description**: Scrapes iPhone products from HKTVmall using Selenium
- **Dependencies**: `selenium`, `webdriver-manager`, `beautifulsoup4`
- **Usage**: `python3 Selenium_hktvmall.py`

#### 5.2 **Playwright Version** (`Plaaywright_hktvmall.py`)
- **Description**: Scrapes iPhone products from HKTVmall using Playwright
- **Dependencies**: `playwright`, `beautifulsoup4`
- **Usage**: `python3 Plaaywright_hktvmall.py`

### 6. **Robot Detection Example** (`Robot_Detection_Example.py`)
- **Description**: Demonstrates handling of bot detection mechanisms
- **Dependencies**: `playwright`, `beautifulsoup4`, `asyncio`
- **Usage**: `python3 Robot_Detection_Example.py`

## Installation Instructions

### Step 1: Clone the Repository
```bash
git clone https://github.com/ericyerongjun/webscraping.git
cd webscraping
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python3 -m venv webscraping_env

# Activate virtual environment
# On Windows:
webscraping_env\Scripts\activate
# On macOS/Linux:
source webscraping_env/bin/activate
```

### Step 3: Install Dependencies
```bash
# Method 1: Install individual packages
pip install playwright beautifulsoup4 selenium webdriver-manager reportlab fake-useragent requests

# Method 2: Use requirements.txt (if you created one)
pip install -r requirements.txt
```

### Step 4: Install Playwright Browsers
```bash
playwright install chromium
```

**Note**: This step may take several minutes as it downloads browser binaries (~100-200MB).

### Step 5: Verify Installation
Test that all packages are installed correctly:
```bash
python3 test_setup.py
```

This script will check all dependencies and provide clear feedback on what's working and what needs attention.

## Usage Examples

### Running a Simple Scraper
```bash
python3 Beautifulsoup_quotes.py
```

### Running an Async Playwright Scraper
```bash
python3 Berkeley_PhD.py
```

### Running Selenium Scraper
```bash
python3 Selenium_hktvmall.py
```

### Generating PDF Reports
```bash
python3 Bloomberg_Latest_News_pdf_exporter.py
```

## Troubleshooting

### Common Issues and Solutions

1. **ModuleNotFoundError**: Make sure all required packages are installed
   ```bash
   pip install [missing_package_name]
   ```

2. **Playwright browser not found**: Install Playwright browsers
   ```bash
   playwright install
   ```

3. **Chrome driver issues**: The webdriver-manager should handle this automatically, but ensure Chrome is installed

4. **Bot detection**: Some websites may block automated requests. The Bloomberg scrapers include bot detection handling mechanisms.

5. **Timeout errors**: Increase timeout values in the scripts if websites are slow to load

6. **Network connection errors**: Some scripts may fail if running in environments with restricted internet access (like CI/CD pipelines). This is expected behavior.

7. **Permission errors during installation**: Use `--user` flag with pip:
   ```bash
   pip install --user -r requirements.txt
   ```

### Testing Your Setup

Run the included test script to verify your installation:
```bash
python3 test_setup.py
```

Expected output when everything is working:
```
==================================================
Web Scraping Dependencies Test
==================================================
✓ requests
✓ beautifulsoup4
✓ playwright
✓ selenium + webdriver-manager
✓ reportlab
✓ fake-useragent
✓ standard library modules
==================================================
Results: 7 passed, 0 failed
🎉 All packages are installed correctly!
```

### System-Specific Notes

- **Windows**: You may need to install Visual C++ redistributables for some packages
- **macOS**: Some packages might require Xcode command line tools: `xcode-select --install`
- **Linux**: You might need to install additional system packages:
  ```bash
  sudo apt-get install python3-dev python3-pip chromium-browser
  ```

## Files in This Repository

| File | Description | Dependencies | Output |
|------|-------------|--------------|--------|
| `Beautifulsoup_quotes.py` | Simple quotes scraper | requests, beautifulsoup4 | Console output |
| `Berkeley_PhD.py` | UC Berkeley PhD programs | playwright, beautifulsoup4 | Console output |
| `Bloomberg_Latest.py` | Bloomberg news (basic) | playwright, beautifulsoup4, fake-useragent | Console output |
| `Bloomberg_Latest_News_pdf_exporter.py` | Bloomberg to PDF | playwright, beautifulsoup4, reportlab, fake-useragent | PDF file |
| `Bloomber_Latest_News_Scraper_pdf_export_wizard_with_multiple_loadmore.py` | Advanced Bloomberg scraper | playwright, beautifulsoup4, reportlab, fake-useragent | PDF file |
| `Bloomberg_Originals.py` | Bloomberg YouTube videos | playwright, beautifulsoup4 | Console output |
| `Crypto_yf.py` | Yahoo Finance crypto data | playwright, beautifulsoup4 | CSV file |
| `Selenium_hktvmall.py` | HKTVmall products (Selenium) | selenium, webdriver-manager, beautifulsoup4 | Console output |
| `Plaaywright_hktvmall.py` | HKTVmall products (Playwright) | playwright, beautifulsoup4 | Console output |
| `Robot_Detection_Example.py` | Bot detection handling | playwright, beautifulsoup4 | Console output |
| `test_setup.py` | Dependency verification | All packages | Test results |
| `requirements.txt` | Package dependencies | - | - |

## Contributing

Feel free to contribute by:
1. Adding new scraping projects
2. Improving existing scrapers
3. Adding better error handling
4. Updating documentation

## Disclaimer

These scripts are for educational purposes. Always respect websites' robots.txt files and terms of service. Be mindful of rate limiting and avoid overwhelming servers with requests.

## License

This project is open source. Please check individual files for specific licensing information.