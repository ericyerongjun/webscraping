#!/usr/bin/env python3
"""
Test script to verify that all required packages are installed correctly.
Run this script to check if your environment is set up properly.
"""

def test_imports():
    """Test importing all required packages."""
    tests = []
    
    # Test basic packages
    try:
        import requests
        tests.append(("✓", "requests"))
    except ImportError as e:
        tests.append(("✗", f"requests - {e}"))
    
    try:
        from bs4 import BeautifulSoup
        tests.append(("✓", "beautifulsoup4"))
    except ImportError as e:
        tests.append(("✗", f"beautifulsoup4 - {e}"))
    
    # Test Playwright
    try:
        from playwright.sync_api import sync_playwright
        from playwright.async_api import async_playwright
        tests.append(("✓", "playwright"))
    except ImportError as e:
        tests.append(("✗", f"playwright - {e}"))
    
    # Test Selenium
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
        tests.append(("✓", "selenium + webdriver-manager"))
    except ImportError as e:
        tests.append(("✗", f"selenium/webdriver-manager - {e}"))
    
    # Test ReportLab
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate
        tests.append(("✓", "reportlab"))
    except ImportError as e:
        tests.append(("✗", f"reportlab - {e}"))
    
    # Test fake-useragent
    try:
        from fake_useragent import UserAgent
        tests.append(("✓", "fake-useragent"))
    except ImportError as e:
        tests.append(("✗", f"fake-useragent - {e}"))
    
    # Test standard library modules
    try:
        import asyncio
        import csv
        import time
        from datetime import datetime
        tests.append(("✓", "standard library modules"))
    except ImportError as e:
        tests.append(("✗", f"standard library - {e}"))
    
    return tests

def main():
    print("=" * 50)
    print("Web Scraping Dependencies Test")
    print("=" * 50)
    
    tests = test_imports()
    
    passed = 0
    failed = 0
    
    for status, package in tests:
        print(f"{status} {package}")
        if status == "✓":
            passed += 1
        else:
            failed += 1
    
    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All packages are installed correctly!")
        print("\nNext steps:")
        print("1. For Playwright scripts, run: playwright install chromium")
        print("2. Ensure you have Chrome browser installed for Selenium scripts")
        print("3. You're ready to run the web scraping projects!")
    else:
        print("❌ Some packages are missing. Please install them using:")
        print("pip install -r requirements.txt")
    
    return failed == 0

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)