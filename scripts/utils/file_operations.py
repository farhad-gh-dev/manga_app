import csv
import pandas as pd
import os

def read_search_words_from_csv(csv_path):
    """
    Read search words from a CSV file.
    Returns a list of search words.
    """
    search_words = []
    try:
        with open(csv_path, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0].strip():  # Check if row exists and first cell is not empty
                    search_words.append(row[0].strip())
        
        if not search_words:
            print("No search terms found in the CSV file.")
        else:
            print(f"Loaded {len(search_words)} search terms from {csv_path}")
            
        return search_words
    except FileNotFoundError:
        print(f"Error: File '{csv_path}' not found.")
        return []
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []

def save_to_csv(details, filename='output.csv'):
    """Save extracted details to a CSV file."""
    try:
        # Ensure the directory exists
        directory = os.path.dirname(filename)
        if directory:
            os.makedirs(directory, exist_ok=True)
            
        keys = details.keys()
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()
            writer.writerow(details)
        print(f"\nData saved to {filename}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")

def save_to_excel(details, filename='output.xlsx'):
    """Save extracted details to an Excel file."""
    try:
        # Ensure the directory exists
        directory = os.path.dirname(filename)
        if directory:
            os.makedirs(directory, exist_ok=True)
            
        df = pd.DataFrame([details])
        df.to_excel(filename, index=False)
        print(f"\nData saved to {filename}")
    except Exception as e:
        print(f"Error saving to Excel: {e}")