from bs4 import BeautifulSoup
import requests
import pandas as pd

response = requests.get('https://appbrewery.github.io/Zillow-Clone/')
web_page = response.text

soup = BeautifulSoup(web_page, 'html.parser')
property_cards = soup.select(".StyledPropertyCardDataWrapper")

property_links = []
property_prices = []
property_addresses = []

for card in property_cards:
    link_of_property = card.select_one('[data-test="property-card-link"]').get('href')
    price_of_property = card.select_one('[data-test="property-card-price"]')
    property_address = card.select_one('[data-test="property-card-addr"]')
    
   
    property_links.append(link_of_property)
    property_prices.append(price_of_property.getText().replace("/mo", "").split('+')[0] if price_of_property else "N/A")
    property_addresses.append(property_address.getText().replace("|", "").strip() if property_address else "N/A")

#saving the data in excel file
data = {
    'Link': property_links,
    'Price': property_prices,
    'Address': property_addresses
}

path = r'D:/Project/Webscraping/properties.xlsx'
df = pd.DataFrame(data)
df.to_excel(path, index=False)

print(property_links)
print(property_prices)
print(property_addresses)
