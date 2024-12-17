import requests
from urllib.parse import unquote, quote
import json

encoded_url = "https://prod-catalog-product-api.dickssportinggoods.com/v2/search?searchVO=%7B%22pageNumber%22%3A0%2C%22pageSize%22%3A48%2C%22selectedSort%22%3A5%2C%22selectedStore%22%3A%221536%22%2C%22storeId%22%3A%2215108%22%2C%22zipcode%22%3A%2202199%22%2C%22isFamilyPage%22%3Atrue%2C%22mlBypass%22%3Afalse%2C%22snbAudience%22%3A%22%22%2C%22selectedCategory%22%3A%2212301_10594220%22%7D"

decoded_url = unquote(encoded_url)
base_url, searchVO_param = decoded_url.split("searchVO=")

searchVO_json = json.loads(searchVO_param)
page_number = 0
all_data = []

while True:
    searchVO_json["pageNumber"] = page_number
    updated_searchVO = json.dumps(searchVO_json)
    encoded_searchVO = quote(updated_searchVO)
    full_url = f"{base_url}searchVO={encoded_searchVO}"

    response = requests.get(full_url)

    print(f"URL: {full_url}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")  # Debug response here

    if response.status_code != 200:
        print(f"Bad request encountered at pageNumber: {page_number}")
        break

    json_data = response.json()
    if page_number!=341:
        all_data.append(response.text)
        print(f"Fetched pageNumber: {page_number}")
    else:
        print(f"No products found at pageNumber: {page_number}")
        break

    page_number += 1

with open('dicks_products.json', 'w') as file:
    json.dump(all_data, file, indent=4)
