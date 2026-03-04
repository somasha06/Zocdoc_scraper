# Zocdoc Doctor Scraper

This project is a fully automated web scraper built to collect doctor listing data from Zocdoc.com for the following cities:

1. New York City  
2. Philadelphia  
3. Austin  

The scraper extracts structured doctor information, handles pagination across all result pages, removes duplicate entries, and exports everything into a single clean CSV file.

# Data 

For each doctor, the following fields are extracted:

1. pic_url (profile image URL)
2. Name
3. Profile URL
4. Specialty
5. Rating
6. Review Count

All cities are combined into one output file as required.



# Technology Used

- Python 3.10+
- Playwright (for browser automation) this is browser automation tool which is used for opening real browser,click button,fill form
- Asyncio (for asynchronous execution) 
- CSV module (built-in Python library)

I used Playwright because Zocdoc is a JavaScript-rendered website, so a simple requests-based scraper would not work reliably.



## Project Structure

zocdoc_scraper/

    scraper.py
    requirements.txt
    README.md
    zocdoc_doctors.csv  (generated after execution)


# Installation

1. Create a Virtual Environment
py -m venv server
server\Scripts\activate

2. Install Dependencies
pip install -r requirements.txt


3. Install Playwright Browsers
playwright install


This downloads the required Chromium browser used for automation.


# How to Run

```
python scraper.py
```

After execution, the file `zocdoc_doctors.csv` will be generated in the project directory.

---

# Output Format

The CSV file uses `|` as the delimiter:

pic_url | Name | Profile URL | Specialty | Rating | Review Count


- Duplicate doctors are removed using profile URL uniqueness
- Missing values are handled safely
- Ratings and review counts are cleaned to numeric values

# Key Features

1. Asynchronous scraping using Playwright
2. Handles dynamic JavaScript-rendered content
3. Automatically traverses pagination
4. Supports multiple cities
5. Prevents duplicate entries
6. Cleans extracted text values
7. Gracefully handles missing fields
8. Detects anti-bot verification pages and exits safely
9. Combines all results into a single CSV file



# Note on Anti-Bot Protection

Zocdoc implements strong anti-bot and IP-based rate limiting mechanisms.

During development, automated access may trigger verification challenges. The scraper includes logic to detect such cases and stop safely.

If blocked, running the scraper from a different network or a US-based cloud environment may be required.

---


