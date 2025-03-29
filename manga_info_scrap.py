import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import time
import sys


# Configuration
AUTO_SELECT_FIRST_ITEM = True  # Set to True to auto-select the first item, False to prompt user

def search_and_select(search_url):
    """
    Fetch search results from a URL and select an item based on configuration.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        print(f"Fetching search results from: {search_url}")
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.select('div.item')
        
        if not results:
            print("No results found.")
            sys.exit(1)
        
        if AUTO_SELECT_FIRST_ITEM:
            selected_item = results[0]
            print("Auto-selected the first item.")
        else:
            display_count = min(10, len(results))
            print(f"\nFound {len(results)} results. Showing first {display_count}:")
            
            for i in range(display_count):
                title_elem = results[i].select_one('a.item-title')
                title = title_elem.get_text(strip=True) if title_elem else f"Item {i+1} (Title not found)"
                print(f"{i+1}. {title}")
            
            while True:
                try:
                    selection = int(input("\nEnter the number for target result: "))
                    if 1 <= selection <= display_count:
                        selected_item = results[selection-1]
                        break
                    else:
                        print(f"Please enter a number between 1 and {display_count}")
                except ValueError:
                    print("Please enter a valid number")
        
        link_elem = selected_item.select_one('a') or selected_item.select_one('a.link')
        
        if not link_elem or not link_elem.get('href'):
            print("Could not find the link for the selected item")
            sys.exit(1)
        
        item_url = link_elem.get('href')
        if item_url.startswith('/'):
            from urllib.parse import urlparse
            parsed_url = urlparse(search_url)
            base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
            item_url = base_url + item_url
        
        print(f"\nSelected: {link_elem.get_text(strip=True)}")
        print(f"URL: {item_url}")
        
        return item_url
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the search page: {e}")
        sys.exit(1)

def extract_item_details(item_url):
    """
    Extract details from the item page
    Returns: Dictionary containing item details
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Add a slight delay to avoid hitting rate limits
        time.sleep(1)
        
        # Fetch the item page
        print(f"\nFetching item details from: {item_url}")
        response = requests.get(item_url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Initialize details dictionary and extract information
        details = {}
        
        # Title
        title_elem = soup.select_one('h3.item-title')
        if title_elem:
            details['title'] = title_elem.get_text(strip=True)
        
        # Author
        author = soup.find('b', string='Authors:').parent.find('a')
        if author:
            details['author'] = author.get_text(strip=True)


        # Artist
        artist = soup.find('b', string='Artists:').parent.find('a')
        if artist:
            details['artist'] = artist.get_text(strip=True)

        # Genres
        genres = soup.find('b', string='Genres:').parent.find('span')
        if genres:
            details['genres'] = genres.get_text(strip=True).split(',')

        # Language
        language = soup.find('b', string='Translated language:').parent.find('span')
        if language:
            details['language'] = language.get_text(strip=True)
        
        # Status
        status = soup.find('b', string='Upload status:').parent.find('span')
        if status:
            details['status'] = status.get_text(strip=True)

        # Release Date  
        release_date = soup.find('b', string='Year of Release:').parent.find('span')
        if release_date:
            details['release_date'] = release_date.get_text(strip=True)

        #Description
        description = soup.select_one('div#limit-height-body-summary')
        if description:
            details['description'] = description.get_text(strip=True).replace('\n', ' ').strip()
        
        # Chapters
        chapters_container = soup.select_one('div.episode-list').select_one('div.main')
        if chapters_container:
            chapters = []
            for chapter in chapters_container.select('div.p-2.d-flex.flex-column.flex-md-row.item'):
                chapter_title_elem = chapter.select_one('a')
                chapter_title = chapter_title_elem.get_text(strip=True) if chapter_title_elem else "Unknown Chapter"
                chapter_url = chapter_title_elem.get('href') if chapter_title_elem else None
                chapters.append({'title': chapter_title, 'url': "https://mto.to" + chapter_url})
            details['chapters'] = chapters
        
        
        
        return details
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the item details: {e}")
        return None

def save_to_csv(details, filename='output.csv'):
    """Save extracted details to a CSV file."""
    keys = details.keys()
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerow(details)
    print(f"\nData saved to {filename}")

def save_to_excel(details, filename='output.xlsx'):
    """Save extracted details to an Excel file."""
    df = pd.DataFrame([details])
    df.to_excel(filename, index=False)
    print(f"\nData saved to {filename}")

def main():
    item_url = search_and_select('https://mto.to/search?word=Home')
    if item_url:
        details = extract_item_details(item_url)
        if details:
            print("\nExtracted Details:")
            for key, value in details.items():
                if key != 'properties':
                    print(f"{key}: {value}")
            if 'properties' in details:
                print("\nProperties:")
                for key, value in details['properties'].items():
                    print(f"  {key}: {value}")
            
            # Save to CSV
            save_to_csv(details)

if __name__ == "__main__":
    main()