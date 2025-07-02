import os, sys, uuid, shutil
from pathlib import Path
import geopandas as gpd
import pandas as pd
import requests
from requests.adapters import HTTPAdapter, Retry
import multiprocessing
from joblib import Parallel, delayed
from tqdm import tqdm
from bs4 import BeautifulSoup
from urllib.parse import urljoin


SESSION = requests.Session()
__retry = Retry(
    total=10, backoff_factor=0.5, 
    status_forcelist=[429, 500, 502, 503, 504]
)
__adapter = HTTPAdapter(max_retries=__retry)
SESSION.mount('https://', __adapter)
# __lock = multiprocessing.Manager().Lock()


def download_footprint(dl_root, url):
    """
    Downloads a footprint from the given URL.
    Returns the path to the downloaded footprint.
    """
    footprint_dir = os.path.join(dl_root)
    # print(f"Creating footprint directory {footprint_dir}", file=open('process_log.log', 'a')) # Creating footprint directory .50f955c9-cfc5-4452-9818-63ab31a98fc4
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and not href.endswith('/') and not href.startswith('?') and not href.startswith('/'):
                # print(f"Downloading footprint url from {url}", file=open('process_log.log', 'a'))
                file_url = urljoin(url, href)
                print(f"Downloading footprint href url from {file_url}", file=open('process_log.log', 'a'))
                # file_name = os.path.basename(url, href)
                
                file_response = requests.get(file_url, stream=True)
                file_response.raise_for_status()

                footprint_data = os.path.join(footprint_dir, file_url.split('/')[-1])
                if int(response.headers.get('Content-Length', 0)) > 1024**3:
                    raise RuntimeError('Oversized source file detected.')
                
                response = SESSION.get(file_url, stream=True)

                with open(footprint_data, 'wb') as f:
                    f.write(response.content)
                    print(f"Downloaded footprint writing to {footprint_data}", file=open('process_log.log', 'a'))
                
        return footprint_dir
            
    except requests.RequestException as e:
        print(f"Error downloading footprint: {e}", file=open('proc_err.log', 'a'))
        return None
    
def merge_footprint(footprint_dir, local_dir, working_dir='.'):
    try: 
        geojson_path = os.path.join(local_dir, 'merged_footprints.geojson')
        if os.path.exists(geojson_path):
            print(f"Merging footprint {footprint_dir} with existing local footprint {local_dir}", file=open('process_log.log', 'a'))
            merged_footprint = gpd.read_file(os.path.join(local_dir, 'merged_footprints.geojson'))
            for root, _, files in os.walk(footprint_dir):
                for file in files:
                    print(f"Checking file {file} in footprint directory", file=open('process_log.log', 'a'))
                    if file.endswith('.shp'):
                        file_path = os.path.join(root, file)
                        print(f"Found shapefile {file_path} in footprint directory", file=open('process_log.log', 'a'))
                        # Found shapefile .362d460f-b6d5-4502-8400-bba97cf4d0a7/QB02_20040808211113_1010010003281400_04AUG08211113-M1BS-052800748070_01_P002_u16rf3413_pansh.shp in footprint directory
                        new_footprint = gpd.read_file(file_path)
                        merged_footprint = pd.concat([merged_footprint, new_footprint], ignore_index=True)
                        # merged_footprint = gpd.overlay(merged_footprint, new_footprint, how='union')
            merged_footprint.to_file(os.path.join(local_dir, 'merged_footprints.geojson'), driver='GeoJSON')
        
        else:
            for root, _, files in os.walk(footprint_dir):
                for file in files:
                    if file.endswith('.shp'):
                        file_path = os.path.join(root, file)
                        print(f"Found shapefile {file_path} in footprint directory", file=open('process_log.log', 'a'))
                        # Found shapefile .362d460f-b6d5-4502-8400-bba97cf4d0a7/QB02_20040808211113_1010010003281400_04AUG08211113-M1BS-052800748070_01_P002_u16rf3413_pansh.shp in footprint directory
                        gpd_footprint = gpd.read_file(file_path)
                        gpd_footprint.to_file(geojson_path, driver='GeoJSON')
                        print(f"Converted shapefile {file_path} to GeoJSON {geojson_path}", file=open('process_log.log', 'a'))
                        break
    except Exception as e:
        print(f"Error merging footprint: {e}", file=open('proc_err.log', 'a'))
        return None
    
    return gpd_footprint

def process_footprint(url):
    process_uuid = str(uuid.uuid4())
    dl_root = '.' + process_uuid
    os.makedirs(dl_root)

    result = None
    try:
        footprint = download_footprint(dl_root, url)
        if footprint is not None:
            result = merge_footprint(footprint, local_dir='../../data/footprint', working_dir=dl_root)
    except RuntimeError:
        print(f"Error processing footprint {process_uuid}", file=open('proc_err.log', 'a'))
    
    finally:
        shutil.rmtree(dl_root)
        return result

def get_urls(base_url, output_path):
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    subdirs = []
    for link in soup.find_all('a'):
        href = link.get('href')
        # Skip parent directory
        if href and href.endswith('/') and href != '../' and not href.startswith('/'):
            current_url = urljoin(base_url, href)
            get_urls(current_url)
            subdirs.append(current_url)

    for url in subdirs:
        print(f"{url}", file=open(output_path, 'a'))

def filter_urls(file, pattern, output_path):
    with open(file, 'r') as f:
        urls = f.readlines()
        print(f"{urls}", file=open('alaska_url.txt', 'a'))
    filtered_urls = [url.strip() for url in urls if pattern in url]
    return filtered_urls


def main(base_url, n_workers=20):
    all_output_path='fetch_url.txt'
    pattern='https://arcticdata.io/data/10.18739/A2KW57K57/iwp_shapefile_footprints/high/'
    alaska_output_path = 'alaska_url.txt'

    get_urls(base_url, all_output_path)
    
    # Only get a subset of URLs, such as Alaska
    # filtered_urls = filter_urls(file=output_path, pattern='https://arcticdata.io/data/10.18739/A2KW57K57/iwp_shapefile_footprints/high/alaska/', alaska_output_path = 'alaska_url.txt')
    
    filtered_urls = filter_urls(all_output_path, pattern, alaska_output_path)
    
    mapper = Parallel(n_jobs=n_workers)
    process = delayed(process_footprint)
    processed_footprint = mapper(process(url) for url in tqdm(filtered_urls, desc='Processing footprints', unit='footprint'))
    return processed_footprint


if __name__ == "__main__":
    base_url = 'https://arcticdata.io/data/10.18739/A2KW57K57/iwp_shapefile_footprints/high/'
    main(base_url, n_workers = 1)