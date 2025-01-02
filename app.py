import os
import requests
from bs4 import BeautifulSoup
import json

url = ''
ifps = '/ipfs/...'

metadata_dir = './metadata_json'
if not os.path.exists(metadata_dir):
    os.makedirs(metadata_dir)

response = requests.get(url + ifps)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    png_links = soup.find_all('a', href=True)

    for link in png_links:
        if link['href'].endswith('.png'):
            full_url = url + link['href']
            
            # in -> 保留 pinata 連結，not in -> 保留 IPFS 連結
            if "filename=" in full_url:
                continue
            
            cleaned_url = full_url.split('?')[0]
            # Extract the image name without the extension (e.g., 0 from 0.png)
            image_name = link['href'].split('/')[-1].split('.')[0]

            try:
                with open(f'./metadata/{image_name}', 'r', encoding='utf-8') as file:
                    data = json.load(file)
                
                if "image" in data:
                    data["image"] = cleaned_url
                    print(f"Updated 'image' key in file {image_name}")
                
                with open(f'./metadata/{image_name}', 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)
                    
                with open(f'{metadata_dir}/{image_name}.json', 'w', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False, indent=4)

            except FileNotFoundError:
                print(f"File {image_name} not found.")
            except json.JSONDecodeError:
                print(f"Error decoding JSON in file {image_name}.")
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
