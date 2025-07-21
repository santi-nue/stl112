import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup

# Target URL
URL = "https://danjovi.com/piano/"  # Change to your desired page
DOWNLOAD_FOLDER = "pdf_downloads"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def get_all_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    # Extract all hrefs from <a> tags
    links = [a.get("href") for a in soup.find_all("a", href=True)]
    return links

def is_pdf_link(link):
    return link.lower().endswith(".pdf")

def download_pdf(pdf_url, folder):
    local_filename = os.path.join(folder, pdf_url.split("/")[-1])
    response = requests.get(pdf_url, stream=True)
    with open(local_filename, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    print(f"Downloaded: {local_filename}")

if __name__ == "__main__":
    links = get_all_links(URL)
    for link in links:
        if is_pdf_link(link):
            # Make sure to handle relative URLs
            pdf_url = urljoin(URL, link)
            download_pdf(pdf_url, DOWNLOAD_FOLDER)
