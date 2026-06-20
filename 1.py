from bs4 import BeautifulSoup
import requests
import pandas as pd

response = requests.get('https://appbrewery.github.io/news.ycombinator.com/')
web_page = response.text

soup = BeautifulSoup(web_page, 'html.parser')
title_articles = []
links_articles = []
for article in soup.find_all(name='a', class_='storylink'):
    title_articles.append(article.getText())
    links_articles.append(article.get('href'))

score_articles = [ article.getText().split()[0] for article in soup.find_all(name='span', class_='score')]

#saving the data in excel file
data = {
    'Title': title_articles,
    'Links': links_articles,
    'Score': score_articles
    #'ket': score_articles2
}
path = r'D:/Project/Webscraping/articles.xlsx'

df = pd.DataFrame(data)
df.to_excel(path, index=False)

