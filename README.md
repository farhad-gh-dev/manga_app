# Manga Web Scraping Project

## Overview
This project is designed to scrape manga information from a specified website. It allows users to input search terms either manually or through a CSV file, fetches relevant data, and saves the extracted information in a structured format.

## Project Structure
```
manga_app
├── manga_web_scraping
│   ├── __init__.py
│   ├── manga_info_scrap.py
│   ├── utils
│   │   ├── __init__.py
│   │   ├── csv_handler.py
│   │   ├── scraper.py
│   │   └── file_operations.py
│   ├── config
│   │   ├── __init__.py
│   │   └── settings.py
│   └── tests
│       ├── __init__.py
│       └── test_scraper.py
├── data
│   ├── input
│   └── output
├── requirements.txt
└── README.md
```

## Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd manga_app
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
1. Run the main script to start scraping:
   ```
   python manga_web_scraping/manga_info_scrap.py
   ```
2. Follow the prompts to enter search terms or specify a CSV file containing search terms.

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.