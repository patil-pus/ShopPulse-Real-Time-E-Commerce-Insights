import requests
import json

s = requests.Session()

def get_data(anchor, header):
    setURL = f"https://api.nike.com/discover/product_wall/v1/marketplace/US/language/en/consumerChannelId/d9a5bc42-4b9c-4976-858a-f159cf99c647?path=/w&queryType=PRODUCTS&anchor={anchor}&count=100"
    response = s.get(url=setURL, headers=header)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

if __name__ == "__main__":
    Headers = {
        'nike-api-caller-id': 'nike:dotcom:browse:wall.client:2.0',
        'anonymousid': '5A7CB5FAAF7C1E5B990F4E9D4B901FC5'
    }

    anchor = 0
    all_data = []

    while anchor <= 9900:
        data = get_data(anchor=anchor, header=Headers)
        if data:
            all_data.append(data)
            print(all_data)
        else:
            print(f"No data found for anchor: {anchor}")
        anchor += 100
        print(f"Fetched data for anchor: {anchor}")

    with open('nike_scraper.json', 'w') as jsonfile:
        json.dump(all_data, jsonfile, indent=4)