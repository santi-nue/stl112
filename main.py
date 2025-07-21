import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
from urllib.parse import urljoin, urlparse
from webdriver_manager.chrome import ChromeDriverManager

# Configurable variables
URL = "https://danjovi.com/piano/"  # <-- Change to your target site!
DOWNLOAD_FOLDER = "pdf_downloads"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def get_selenium_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    stealth(
        driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    return driver



def get_all_pdf_links(driver, url):
    driver.get(url)
    time.sleep(5)  # Give JS time to load content; adjust as needed.

    links = [a.get_attribute('href') for a in driver.find_elements("tag name", "a")]
    pdf_links = [link for link in links if link and link.lower().endswith('.pdf')]
    return pdf_links

def requests_with_selenium_cookies(driver, url):
    session = requests.Session()
    # Copy cookies from Selenium to requests
    for cookie in driver.get_cookies():
        session.cookies.set(cookie['name'], cookie['value'])
    # Set a realistic User-Agent
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    })
    response = session.get(url, stream=True, timeout=60)
    return response

def download_pdf(pdf_url, driver, folder):
    filename = os.path.basename(urlparse(pdf_url).path)
    filename = filename or "file.pdf"
    local_filepath = os.path.join(folder, filename)

    print(f"Downloading: {pdf_url}")
    try:
        response = requests_with_selenium_cookies(driver, pdf_url)
        response.raise_for_status()
        with open(local_filepath, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Saved: {local_filepath}")
    except Exception as e:
        print(f"Failed to download {pdf_url}: {e}")

if __name__ == "__main__":
    driver = get_selenium_driver()
    try:
        pdf_links = get_all_pdf_links(driver, URL)
        print(f"Found {len(pdf_links)} PDF links.")
        for pdf in pdf_links:
            full_pdf_url = urljoin(URL, pdf)
            download_pdf(full_pdf_url, driver, DOWNLOAD_FOLDER)
    finally:
        driver.quit()
