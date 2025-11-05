import requests
import re
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

def extract_emails_from_site(url, max_depth=1):
    """
    Extract email addresses from a website by scraping the page and optionally following links.
    
    Args:
    url (str): The starting URL to scrape.
    max_depth (int): Maximum depth for following links (default: 1, just the main page).
    
    Returns:
    set: A set of unique email addresses found.
    """
    emails = set()
    visited = set()
    
    def scrape_page(current_url, depth):
        if depth > max_depth or current_url in visited:
            return
        visited.add(current_url)
        
        try:
            response = requests.get(current_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract emails from text using regex
            text = soup.get_text()
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            found_emails = re.findall(email_pattern, text)
            emails.update(found_emails)
            
            # Follow links if depth allows
            if depth < max_depth:
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    full_url = urljoin(current_url, href)
                    if urlparse(full_url).netloc == urlparse(url).netloc:  # Stay on same domain
                        scrape_page(full_url, depth + 1)
                        
        except requests.RequestException as e:
            print(f"Error scraping {current_url}: {e}")
    
    scrape_page(url, 0)
    return emails

# Example usage
if __name__ == "__main__":
    site_url = "https://example.com"  # Replace with the target site
    found_emails = extract_emails_from_site(site_url)
    print("Found emails:")
    for email in found_emails:
        print(email)