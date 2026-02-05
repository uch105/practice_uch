import requests
from bs4 import BeautifulSoup
import json
import time
import random
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',

    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Mozilla/5.0 (X11; Linux i686; rv:109.0) Gecko/20100101 Firefox/115.0',

    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',

    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',

    'Mozilla/5.0 (Linux; Android 10; SM-A505FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone14,3; U; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Mobile/19A346 Safari/602.1'
]

headers = {
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://medex.com.bd/',
    'DNT': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, br'
}

def clean_split(text):
    return [item.strip() for item in text.split('\n') if item.strip()]

drugs_list = []

start_from = 1
if os.path.exists('progress.txt'):
    with open('progress.txt', 'r') as f:
        start_from = int(f.read())

for i in range(start_from, 2472):
    try:
        time.sleep(random.uniform(1, 3))
        headers['User-Agent'] = random.choice(user_agents)
        
        url = f"https://medex.com.bd/generics/{str(i)}"
        session = requests.Session()
        response = session.get(url, headers=headers)
            
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        drug_name = soup.find(class_='page-heading-1-l').text.strip()

        ac_headers = soup.find_all(class_='ac-header')
        ac_bodies = soup.find_all(class_='ac-body')
        
        drug_data = {"name": drug_name}

        for j in range(min(len(ac_headers), len(ac_bodies))):
            header_text = ac_headers[j].text.strip().lower().replace(" ", "_")
            body_text = clean_split(ac_bodies[j].text)
            drug_data[header_text] = body_text
        
        drugs_list.append(drug_data)
        
        if i % 10 == 0:
            with open('drugs_database_temp.json', 'w', encoding='utf-8') as f:
                json.dump({"drugs": drugs_list}, f, indent=2, ensure_ascii=False)
            with open('progress.txt', 'w') as f:
                f.write(str(i))
    
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch page {i}: {e}")
        
    except Exception as e:
        print(f"❌ Error at {i}: {str(e)[:100]}...")
        time.sleep(10)
        continue

with open('drugs_database.json', 'w', encoding='utf-8') as f:
    json.dump({"drugs": drugs_list}, f, indent=2, ensure_ascii=False)

print("Scraping complete. Data saved to drugs_database.json")
