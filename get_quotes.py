import requests
import json
api_url = 'https://api.api-ninjas.com/v1/quotes'
count = 1137

with open('quotes.txt', 'a', encoding='utf-8') as f:
    for i in range(3681):
        if count%100 == 0:
            print(f"{count} quote added")
        try:
            response = requests.get(api_url, headers={'X-Api-Key': 'exdnTVLTOcBr76peuqSGtw==SbhIVYoTgbkLR3R1'})
            if response.status_code == requests.codes.ok:
                quote_data = response.json()
                f.write(f'"{quote_data[0]["quote"]}" - {quote_data[0]["author"]}\n')
                count +=1
            else:
                break
        except:
            break
print(f"{count} quotes added!")
