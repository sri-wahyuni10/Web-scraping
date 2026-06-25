from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

# 1. AMBIL DAFTAR KATEGORI DARI HALAMAN UTAMA (Mencegah AttributeError / NoneType)
url_utama = 'https://books.toscrape.com/'
response_utama = requests.get(url_utama).text
soup_utama = BeautifulSoup(response_utama, 'html.parser')

# Temukan sidebar kategori dari halaman utama
sidebar = soup_utama.find('div', class_ = 'side_categories')

all_links_categorybooks = []
name_category = []

# Ambil semua link dari sidebar
for link in sidebar.find_all('a'):
    name_of_category = link.get_text(strip=True)
    if name_of_category == "Books": continue # Lewati kategori induk
        
    full_url = 'https://books.toscrape.com/' + link.get('href')
    all_links_categorybooks.append(full_url)
    name_category.append(name_of_category)

# 2. PROSES SCRAPING DAN PENYIMPANAN EXCEL
path_excel = r'D:/Project/Webscraping/books_by_category.xlsx'

# Buka ExcelWriter sekali saja di LUAR loop untuk multi-sheet
with pd.ExcelWriter(path_excel, engine='openpyxl') as writer:
    for i, links in enumerate(all_links_categorybooks):
        nama_kategori_sekarang = name_category[i]
        print(f"Sedang mengambil data untuk kategori: {nama_kategori_sekarang}")
        
        response_kategori = requests.get(links)
        if response_kategori.status_code != 200: continue
            
        soup_category = BeautifulSoup(response_kategori.text, "html.parser")
        
        # PERBAIKAN: Cari buku di halaman kategori spesifik
        all_books = soup_category.find_all('article', class_='product_pod')
        
        books_in_this_category = []
        for book in all_books:
            title = book.find('h3').find('a').get('title')
            price = book.find('p', class_='price_color').text
            availability = book.find('p', class_='instock availability').text.strip()
            
            books_in_this_category.append({
                'Title': title, 'Price': price, 'Availability': availability, 'Category': nama_kategori_sekarang
            })
            
        # Simpan per kategori ke sheet yang berbeda
        if books_in_this_category:
            df = pd.DataFrame(books_in_this_category)
            nama_sheet_aman = nama_kategori_sekarang[:30] # Limit 31 karakter
            df.to_excel(writer, sheet_name=nama_sheet_aman, index=False)
            print(f"-> Sukses menyimpan sheet '{nama_sheet_aman}'.")
            
        time.sleep(1) # Jeda sopan

print("\nProses Selesai!")
