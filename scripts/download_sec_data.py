import requests
from bs4 import BeautifulSoup
import os
import zipfile
import io
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

def extract_and_upload_to_s3():
    download_dir = "ceac_financial_statements"
    os.makedirs(download_dir, exist_ok=True)

    ceac_url = "https://www.sec.gov/data-research/sec-markets-data/financial-statement-data-sets"

    headers = {
        "User-Agent": "Riya_User/1.0 (your_mail@example.com)"
    }
    web_response = requests.get(ceac_url, headers=headers)
    if web_response.status_code == 200:
        soup = BeautifulSoup(web_response.text, 'html.parser')
        zip_links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.endswith('.zip'):
                full_url = "https://www.sec.gov" + href if href.startswith("/") else href
                zip_links.append(full_url)

        if zip_links:
            s3_hook = S3Hook(aws_conn_id="aws_default")

            for zip_link in zip_links:
                zip_filename = zip_link.split("/")[-1]  
                zip_folder_name = zip_filename.replace(".zip", "") 

                print(f"Downloading: {zip_link}")
                zip_response = requests.get(zip_link, headers=headers)

                if zip_response.status_code == 200:
                    try:
                        zip_bytes = io.BytesIO(zip_response.content)

                        
                        with zipfile.ZipFile(zip_bytes, "r") as z:
                            for file_name in z.namelist():
                                file_bytes = z.read(file_name)
                                s3_file_key = f"ceac_financial_statements/{zip_folder_name}/{file_name}"
                                s3_hook.load_bytes(file_bytes, key=s3_file_key, bucket_name="s3-airflow-bucket-1", replace=True)
                                print(f"Uploaded extracted file to S3: {s3_file_key}")

                    except zipfile.BadZipFile:
                        print(f"Skipping invalid ZIP file: {zip_filename}")
                else:
                    print(f"Failed to download zip file: {zip_link} - Status Code: {zip_response.status_code}")
        else:
            print("No ZIP links found on the webpage.")
    else:
        print(f"Failed to access the website. Status Code: {web_response.status_code}")

    print("All extracted files have been uploaded to S3.")
