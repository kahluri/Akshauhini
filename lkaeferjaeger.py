import requests
import time
from tqdm import tqdm

# Define a dictionary with URLs and filenames
files = {
    "amazon.txt": "http://kaeferjaeger.gay/sni-ip-ranges/amazon/ipv4_merged_sni.txt",
    "digitalocean.txt": "https://kaeferjaeger.gay/sni-ip-ranges/digitalocean/ipv4_merged_sni.txt",
    "google.txt": "https://kaeferjaeger.gay/sni-ip-ranges/google/ipv4_merged_sni.txt",
    "oracle.txt": "https://kaeferjaeger.gay/sni-ip-ranges/oracle/ipv4_merged_sni.txt",
    "microsoft.txt": "https://kaeferjaeger.gay/sni-ip-ranges/microsoft/ipv4_merged_sni.txt"
}

# Function to download a file with a progress bar
def download_file(url, filename):
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(filename, 'wb') as file, tqdm(
        desc=filename,
        total=total_size,
        unit='B',
        unit_scale=True,
        unit_divisor=1024
    ) as bar:
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                file.write(chunk)
                bar.update(len(chunk))
    
    print(f"Downloaded {filename} successfully.")

# Loop through the dictionary and download each file one by one
for filename, url in files.items():
    print(f"Downloading {filename} from {url}")
    try:
        download_file(url, filename)
    except Exception as e:
        print(f"Failed to download {filename}: {e}")
    time.sleep(2)  # Add a delay to avoid overwhelming the server

