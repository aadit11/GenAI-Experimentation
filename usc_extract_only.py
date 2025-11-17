

import requests
from bs4 import BeautifulSoup
import time
import re
import csv
import os
from typing import List, Set
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import logging
import argparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

USC_DIRECTORY_URL = "https://uscdirectory.usc.edu/web/directory/faculty-staff/"
DELAY_BETWEEN_REQUESTS = 2


class USCDirectoryExtractor:
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.driver = None
        self.emails: Set[str] = set()
        
    def setup_selenium(self, headless=True):
        chrome_options = Options()
        if headless:
            chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        logger.info("Selenium WebDriver initialized")
    
    def extract_emails_from_text(self, text: str) -> Set[str]:
        email_patterns = [
            r'\b[A-Za-z0-9._%+-]+@usc\.edu\b',  
            r'[A-Za-z0-9._%+-]+@usc\.edu',  
            r'mailto:([A-Za-z0-9._%+-]+@usc\.edu)',  
            r'"([A-Za-z0-9._%+-]+@usc\.edu)"',  
            r"'([A-Za-z0-9._%+-]+@usc\.edu)'",  
            r'<([A-Za-z0-9._%+-]+@usc\.edu)>',  
            r'\(([A-Za-z0-9._%+-]+@usc\.edu)\)',  
            r'\[([A-Za-z0-9._%+-]+@usc\.edu)\]',  
        ]
        
        emails = set()
        for pattern in email_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                email = match if isinstance(match, str) else match[0] if match else None
                if email:
                    email = email.lower().strip()
                    if email.endswith('@usc.edu'):
                        username = email.split('@')[0]
                        if username and len(username) > 0:
                            emails.add(email)
        
        return emails
    
    def scrape_with_requests(self) -> Set[str]:
        logger.info("Attempting to scrape with requests...")
        try:
            response = self.session.get(USC_DIRECTORY_URL, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            page_text = soup.get_text()
            emails = self.extract_emails_from_text(page_text)
            
            email_links = soup.find_all('a', href=re.compile(r'mailto:.*@usc\.edu', re.IGNORECASE))
            for link in email_links:
                email = link.get('href', '').replace('mailto:', '').strip()
                if email and email.lower().endswith('@usc.edu'):
                    emails.add(email.lower())
            
            logger.info(f"Found {len(emails)} emails with requests method")
            return emails
            
        except Exception as e:
            logger.error(f"Error scraping with requests: {e}")
            return set()
    
    def extract_emails_from_page(self, wait_time=5) -> Set[str]:
        emails = set()
        
        try:
            logger.info("Waiting for page content to load...")
            time.sleep(3)
            
            logger.info("Extracting emails from page source using regex...")
            page_source = self.driver.page_source
            page_emails = self.extract_emails_from_text(page_source)
            emails.update(page_emails)
            logger.info(f"Found {len(page_emails)} emails in page source")
            
            try:
                body_text = self.driver.find_element(By.TAG_NAME, "body").text
                text_emails = self.extract_emails_from_text(body_text)
                emails.update(text_emails)
                logger.info(f"Found {len(text_emails)} emails in visible text")
            except Exception as e:
                logger.debug(f"Error extracting from body text: {e}")
            
            try:
                email_links = self.driver.find_elements(By.XPATH, "//a[contains(@href, 'mailto:') and contains(@href, '@usc.edu')]")
                for link in email_links:
                    href = link.get_attribute('href') or ''
                    found_emails = self.extract_emails_from_text(href)
                    emails.update(found_emails)
                    link_text = link.text or ''
                    found_emails = self.extract_emails_from_text(link_text)
                    emails.update(found_emails)
                logger.info(f"Found {len(email_links)} @usc.edu email links")
            except Exception as e:
                logger.debug(f"Error finding mailto links: {e}")
            
            try:
                all_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), '@usc.edu') or contains(@href, '@usc.edu')]")
                for element in all_elements:
                    text = element.text or element.get_attribute('innerHTML') or element.get_attribute('outerHTML') or element.get_attribute('href') or ''
                    found_emails = self.extract_emails_from_text(text)
                    emails.update(found_emails)
                logger.info(f"Checked {len(all_elements)} elements containing '@usc.edu'")
            except Exception as e:
                logger.debug(f"Error checking all elements: {e}")
            
            try:
                tables = self.driver.find_elements(By.TAG_NAME, "table")
                for table in tables:
                    table_text = table.text
                    table_html = table.get_attribute('outerHTML')
                    found_emails = self.extract_emails_from_text(table_text + " " + (table_html or ""))
                    emails.update(found_emails)
                logger.info(f"Checked {len(tables)} tables")
            except Exception as e:
                logger.debug(f"Error extracting from tables: {e}")
            
            try:
                last_height = self.driver.execute_script("return document.body.scrollHeight")
                scroll_pause = 1
                scrolls = 0
                max_scrolls = 5
                
                while scrolls < max_scrolls:
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(scroll_pause)
                    
                    page_source = self.driver.page_source
                    scroll_emails = self.extract_emails_from_text(page_source)
                    emails.update(scroll_emails)
                    
                    new_height = self.driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height
                    scrolls += 1
                
                logger.info(f"Scrolled {scrolls} times, found additional emails")
            except Exception as e:
                logger.debug(f"Error scrolling: {e}")
            
        except Exception as e:
            logger.warning(f"Error extracting emails from results: {e}")
        
        return emails
    
    def perform_search(self, search_term="", wait_after=3):
        try:
            time.sleep(2)
            
            search_selectors = [
                "input[type='text']",
                "input[name*='search']",
                "input[id*='search']",
                "input[type='search']"
            ]
            
            search_input = None
            for selector in search_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        search_input = elements[0]
                        logger.info(f"Found search input using selector: {selector}")
                        break
                except:
                    continue
            
            if not search_input:
                try:
                    search_input = self.driver.find_element(By.XPATH, "//input[@type='text' or @type='search']")
                except:
                    pass
            
            if search_input:
                search_input.clear()
                if search_term:
                    search_input.send_keys(search_term)
                else:
                    search_input.send_keys("*")
                
                time.sleep(1)
                
                search_button = None
                button_selectors = [
                    "button[type='submit']",
                    "input[type='submit']",
                    "//button[contains(text(), 'Search')]",
                    "//input[@value='Search']"
                ]
                
                for selector in button_selectors:
                    try:
                        if selector.startswith("//"):
                            elements = self.driver.find_elements(By.XPATH, selector)
                        else:
                            elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                        if elements:
                            search_button = elements[0]
                            break
                    except:
                        continue
                
                if search_button:
                    search_button.click()
                    logger.info(f"Clicked search button with term: '{search_term if search_term else '*'}''")
                    time.sleep(wait_after)
                    return True
                else:
                    search_input.send_keys(Keys.RETURN)
                    time.sleep(wait_after)
                    return True
            else:
                logger.warning("Could not find search input field")
                return False
                
        except Exception as e:
            logger.warning(f"Error performing search: {e}")
            return False
    
    def scrape_with_selenium(self, headless=True, search_keyword="manager") -> Set[str]:
        logger.info(f"Attempting to scrape with Selenium (searching for: '{search_keyword}')...")
        
        if not self.driver:
            self.setup_selenium(headless=headless)
        
        all_emails = set()
        
        try:
            self.driver.get(USC_DIRECTORY_URL)
            logger.info(f"Loaded page: {self.driver.title}")
            time.sleep(3)
            
            logger.info(f"Searching for keyword: '{search_keyword}'...")
            if self.perform_search(search_keyword, wait_after=5):
                logger.info("Waiting for search results to load...")
                time.sleep(5)

                emails = self.extract_emails_from_page(wait_time=8)
                all_emails.update(emails)
                logger.info(f"Found {len(emails)} @usc.edu emails from '{search_keyword}' search results")
                
                page_num = 1
                max_pages = 10  
                
                while page_num < max_pages:
                    try:
                        next_buttons = self.driver.find_elements(
                            By.XPATH,
                            "//a[contains(text(), 'Next') or contains(text(), '>') or contains(@class, 'next')]"
                        )
                        
                        if not next_buttons:
                            page_links = self.driver.find_elements(
                                By.XPATH,
                                f"//a[contains(text(), '{page_num + 1}') and contains(@href, 'page')]"
                            )
                            if page_links:
                                next_buttons = page_links
                        
                        if next_buttons:
                            btn_class = next_buttons[0].get_attribute('class') or ''
                            if 'disabled' not in btn_class.lower():
                                logger.info(f"Navigating to page {page_num + 1}...")
                                next_buttons[0].click()
                                time.sleep(5) 
                                
                                page_emails = self.extract_emails_from_page(wait_time=5)
                                if page_emails:
                                    all_emails.update(page_emails)
                                    logger.info(f"Page {page_num + 1}: Found {len(page_emails)} additional emails (total: {len(all_emails)})")
                                    page_num += 1
                                else:
                                    logger.info(f"No more emails found on page {page_num + 1}, stopping pagination")
                                    break
                            else:
                                logger.info("Next button is disabled, stopping pagination")
                                break
                        else:
                            logger.info("No more pages found, stopping pagination")
                            break
                    except Exception as e:
                        logger.debug(f"Error checking for pagination: {e}")
                        break
                
            else:
                logger.warning(f"Failed to perform search for '{search_keyword}'")
            
            if not all_emails:
                logger.info("No emails from search, trying to extract from initial page...")
                self.driver.get(USC_DIRECTORY_URL)
                time.sleep(3)
                emails = self.extract_emails_from_page(wait_time=5)
                all_emails.update(emails)
                logger.info(f"Found {len(emails)} emails from initial page")
            
            logger.info(f"Total unique @usc.edu emails found: {len(all_emails)}")
            return all_emails
            
        except Exception as e:
            logger.error(f"Error scraping with Selenium: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return all_emails
        finally:
            if self.driver:
                self.driver.quit()
    
    def extract_directory(self, headless=True, use_selenium=True, search_keyword="manager") -> Set[str]:
        logger.info(f"Starting directory extraction (searching for: '{search_keyword}')...")
        
        if use_selenium:
            emails = self.scrape_with_selenium(headless=headless, search_keyword=search_keyword)
            if not emails:
                logger.info("Selenium found no emails, trying requests method...")
                emails = self.scrape_with_requests()
        else:
            emails = self.scrape_with_requests()
            if not emails:
                logger.info("Requests found no emails, trying Selenium method...")
                emails = self.scrape_with_selenium(headless=headless, search_keyword=search_keyword)
        
        self.emails = emails
        logger.info(f"Total unique @usc.edu emails found: {len(self.emails)}")
        return self.emails
    
    def save_to_csv(self, filename: str, include_headers: bool = True):
        if not self.emails:
            logger.warning("No emails to save")
            return
        
        emails_list = sorted(list(self.emails))
        
        file_exists = os.path.exists(filename)
        existing_emails = set()
        
        if file_exists:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        if 'email' in row:
                            existing_emails.add(row['email'].lower())
            except:
                pass
        
        new_emails = []
        for email in emails_list:
            if email.lower() not in existing_emails:
                username = email.split('@')[0].replace('.', ' ').title()
                new_emails.append({
                    'email': email,
                    'name': username,
                    'domain': 'usc.edu',
                    'username': email.split('@')[0]
                })
        
        if not new_emails and file_exists:
            logger.info(f"All {len(emails_list)} emails already exist in {filename}")
            return
        
        write_headers = include_headers and (not file_exists or not new_emails)
        
        with open(filename, 'a' if file_exists and new_emails else 'w', newline='', encoding='utf-8') as f:
            fieldnames = ['email', 'name', 'domain', 'username']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            
            if write_headers:
                writer.writeheader()
            
            if new_emails:
                writer.writerows(new_emails)
                logger.info(f"Saved {len(new_emails)} new emails to {filename}")
            else:
                for email in emails_list:
                    username = email.split('@')[0].replace('.', ' ').title()
                    writer.writerow({
                        'email': email,
                        'name': username,
                        'domain': 'usc.edu',
                        'username': email.split('@')[0]
                    })
                logger.info(f"Saved {len(emails_list)} emails to {filename}")


def main():
    parser = argparse.ArgumentParser(description='Extract @usc.edu emails from USC Directory')
    parser.add_argument('-o', '--output', type=str, default='usc_emails.csv',
                       help='Output CSV filename (default: usc_emails.csv)')
    parser.add_argument('-k', '--keyword', type=str, default='manager',
                       help='Search keyword to use (default: manager)')
    parser.add_argument('--no-headless', action='store_true',
                       help='Run browser in visible mode (for debugging)')
    parser.add_argument('--no-selenium', action='store_true',
                       help='Use only requests library (no browser)')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("USC Directory Email Extractor")
    print("=" * 60)
    print(f"\nSearch Keyword: '{args.keyword}'")
    print("\n⚠️  LEGAL WARNING:")
    print("This script is for educational purposes only.")
    print("Review USC's Terms of Service before scraping.")
    print("=" * 60)
    

    extractor = USCDirectoryExtractor()
    

    print(f"\nStarting extraction (searching for '{args.keyword}')...")
    headless_mode = not args.no_headless
    use_selenium = not args.no_selenium
    
    emails = extractor.extract_directory(
        headless=headless_mode, 
        use_selenium=use_selenium,
        search_keyword=args.keyword
    )
    
    usc_emails = {email for email in emails if email.endswith('@usc.edu')}
    if len(usc_emails) != len(emails):
        logger.info(f"Filtered out {len(emails) - len(usc_emails)} non-@usc.edu emails")
    emails = usc_emails
    
    if not emails:
        print("\n❌ No @usc.edu emails found. The directory structure may have changed.")
        print("You may need to customize the scraping logic.")
        return
    
    print(f"\n✅ Found {len(emails)} unique @usc.edu email addresses (from '{args.keyword}' search)")
    print("\nFirst 10 emails:")
    for email in sorted(list(emails))[:10]:
        print(f"  - {email}")
    
    output_file = args.output
    extractor.save_to_csv(output_file)
    
    print("\n" + "=" * 60)
    print(f"✅ Extraction complete!")
    print(f"📄 CSV file saved to: {output_file}")
    print(f"📊 Total @usc.edu emails found: {len(emails)}")
    print(f"🔍 Search keyword used: '{args.keyword}'")
    print("=" * 60)


if __name__ == "__main__":
    main()

