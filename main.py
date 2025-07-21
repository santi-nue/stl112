from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import os
import requests
from urllib.parse import urljoin

URL = "https://danjovi.com/piano/"  # Change to your WordPress site
DOWNLOAD_FOLDER = "pdf_downloads"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode

with webdriver.Chrome(options=chrome_options) as driver:
    driver.get(URL)
    time.sleep(5)  # Wait for JavaScript to load content; adjust if needed

    links = [a.get_attribute('href') for a in driver.find_elements("tag name", "a")]
    pdf_links = [link for link in links if link and link.lower().endswith('.pdf')]

    for link in pdf_links:
        pdf_url = urljoin(URL, link)
        filename = os.path.join(DOWNLOAD_FOLDER, os.path.basename(pdf_url))
        print(f"Downloading {pdf_url}")
        r = requests.get(pdf_url, stream=True)
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
