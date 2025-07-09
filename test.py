import requests
from bs4 import BeautifulSoup
import json

drugs_list = []

def clean_split(text):
    return [item.strip() for item in text.split('\n') if item.strip()]

for i in range(1, 2470):
    try:
        url = f"https://medex.com.bd/generics/{str(i)}"
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        drug_name = soup.find_all(class_='page-heading-1-l')[0].text.strip()
        
        ac_headers = soup.find_all(class_='ac-header')
        ac_bodies = soup.find_all(class_='ac-body')
        
        drug_data = {"name": drug_name}

        for i in range(min(len(ac_headers), len(ac_bodies))):
            header_text = ac_headers[i].text.strip().lower().replace(" ", "_")
            body_text = clean_split(ac_bodies[i].text)
            drug_data[header_text] = body_text
        
        drugs_list.append(drug_data)
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch page {i}: {e}")
    except Exception as e:
        print(f"Error processing page {i}: {e}")

# Save to JSON file
with open('drugs_database.json', 'w', encoding='utf-8') as f:
    json.dump({"drugs": drugs_list}, f, indent=2, ensure_ascii=False)

print("Scraping complete. Data saved to drugs_database.json")
