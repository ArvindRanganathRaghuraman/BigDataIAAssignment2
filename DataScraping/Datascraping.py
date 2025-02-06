import requests
from bs4 import BeautifulSoup
from io import BytesIO
import os
import zipfile


download_dir = "ceac_financial_statements"
os.makedirs(download_dir, exist_ok=True)


ceac_url = "https://www.sec.gov/data-research/sec-markets-data/financial-statement-data-sets"


headers = {
    "User-Agent": "Arvind/1.0 (your_mail@example.com)"
}


# Step 1: Fetch the SEC webpage and extract ZIP file links
web_response = requests.get(ceac_url, headers=headers)

if web_response.status_code == 200:
    soup = BeautifulSoup(web_response.text, 'html.parser')

    zip_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.endswith('.zip'):
            full_url = "https://www.sec.gov" + href if href.startswith("/") else href
            zip_links.append(full_url)

    

    
    for zip_link in zip_links:
        zip_filename = os.path.join(download_dir, zip_link.split("/")[-1])

        print(f" Downloading: {zip_link}")
        zip_response = requests.get(zip_link, headers=headers)

        if zip_response.status_code == 200:
            with open(zip_filename, "wb") as f:
                f.write(zip_response.content)
            print(f"Saved: {zip_filename}")

            
            try:
                with zipfile.ZipFile(zip_filename, "r") as z:
                    z.extractall(download_dir)
                    print(f" Extracted contents of {zip_filename}")
            except zipfile.BadZipFile:
                print(f" Skipping invalid ZIP file: {zip_filename}")
        else:
            print(f"Failed to download zip file: {zip_link} - Status Code: {zip_response.status_code}")

else:
    print(f"Failed to access the website. Status Code: {web_response.status_code}")

print(f" All extracted files are saved in: {download_dir}")
