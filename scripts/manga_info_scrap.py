import sys
import os
import time
from urllib.parse import quote

# Add the current directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.scraper import search_and_select, extract_item_details
from utils.file_operations import save_to_csv, read_search_words_from_csv
from config.settings import DEFAULT_INPUT_CSV_PATH, DEFAULT_OUTPUT_DIRECTORY, BASE_SEARCH_URL, WAIT_BETWEEN_SEARCHES

def main():
    try:
        # Ensure output directory exists
        os.makedirs(DEFAULT_OUTPUT_DIRECTORY, exist_ok=True)
        
        print("How would you like to input search terms?")
        print("1. Enter a single search term")
        print(f"2. Read from the default CSV file ({DEFAULT_INPUT_CSV_PATH})")
        print("3. Read from a custom CSV file")
        
        choice = input("Enter your choice (1, 2, or 3): ")
        
        search_words = []
        if choice == "1":
            search_word = input("Please enter the search word: ")
            search_words = [search_word]
        elif choice == "2":
            # Convert relative path to absolute path
            abs_input_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), DEFAULT_INPUT_CSV_PATH)
            print(f"Reading search terms from default CSV: {abs_input_path}")
            search_words = read_search_words_from_csv(abs_input_path)
            print(f"Found {len(search_words)} search terms.")
            if not search_words:
                print("No valid search terms found in the CSV.")
                return
        elif choice == "3":
            csv_path = input("Enter the path to the CSV file: ")
            print(f"Reading search terms from CSV: {csv_path}")
            search_words = read_search_words_from_csv(csv_path)
            print(f"Found {len(search_words)} search terms.")
            if not search_words:
                print("No valid search terms found in the CSV.")
                return
        else:
            print("Invalid choice. Exiting.")
            return
        
        # Convert relative output path to absolute path
        abs_output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), DEFAULT_OUTPUT_DIRECTORY)
        os.makedirs(abs_output_dir, exist_ok=True)
        
        for i, search_word in enumerate(search_words, 1):
            print(f"\n[{i}/{len(search_words)}] Processing search term: {search_word}")
            
            formatted_word = quote(search_word)
            full_search_url = BASE_SEARCH_URL + formatted_word

            item_url = search_and_select(full_search_url)
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
                    
                    # Create output filename using manga title or search term
                    base_filename = details.get('title', search_word).replace(' ', '_')
                    output_path = os.path.join(abs_output_dir, f"{base_filename}.csv")
                    
                    # Save to the configured output directory
                    save_to_csv(details, output_path)
            
            # Wait between searches if there are more items to process
            if i < len(search_words):
                print(f"Waiting {WAIT_BETWEEN_SEARCHES} seconds before next search...")
                time.sleep(WAIT_BETWEEN_SEARCHES)
        
        print("\nAll search terms processed.")
        print(f"Output files can be found in: {abs_output_dir}")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()  # Print detailed error information
        return

if __name__ == "__main__":
    main()