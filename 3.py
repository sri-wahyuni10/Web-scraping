from bs4 import BeautifulSoup
import requests
import pandas as pd

response = requests.get ("https://www.coingecko.com/en/categories").text
soup = BeautifulSoup(response, "html.parser")

property_tables = soup.find('table')
rows = property_tables.find_all('tr')

data = []   

for row in rows:
    columns = row.find_all('td')
    if len(columns)> 0:
        Category_name = columns[2].text.strip()
        Top_gainers = columns[3].text.strip()
        change_1h = columns[4].text.strip()
        change_24h = columns[5].text.strip()
        link_of_category = 'https://www.coingecko.com/' + columns[2].find('a').get('href')
        
        data.append({
            'Category_name' : Category_name,
            'Top_gainers' : Top_gainers,
            'change_1h' : change_1h,
            'change_24h' : change_24h,
            'link_of_category' : link_of_category
            
        })
        
    path = r'D:/Project/Webscraping/crypto_categories.xlsx'
    df = pd.DataFrame(data)
    df.to_excel(path, index=False)
    
        
