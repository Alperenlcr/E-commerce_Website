from bs4 import BeautifulSoup
import requests
from time import sleep
from app.db_models import add_item_to_db


max_page_number = 1     # sitelerden kacinci sayfalarina kadar veri cekilecegini ayarlamak icin degisken
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0',
    'Accept-Language': 'en-US, en;q=0.5'
}


# hepsiburada sitesi scraping fonksiyonu
def HepsiBurada_digger(base_url, headers):
    items = []
    for i in range(1, 1+max_page_number):   # page number range
        response = requests.get(base_url + '&page={0}'.format(i), headers=headers)      # data for a page

        soup = BeautifulSoup(response.content, 'html.parser')
        results = soup.find_all('a', attrs={'class':'moria-ProductCard-gyqBb'})
        for result in results:
            data = {}
            url = "https://www.hepsiburada.com"+result['href']
            try:
                response = requests.get(url=url, headers=headers)      # data for a page
            except requests.exceptions.ConnectionError:
                sleep(5)

            if 'adservice' not in url:
                soup = BeautifulSoup(response.content, 'html.parser')
                temp = str(soup.find('div', {'class':'key-properties'}))
                data['Title'] = soup.find('h1', {'itemprop':'name'}).text[10:].split('\r')[0]
                data['Price'] = int(''.join(filter(lambda x: x.isdigit(), soup.find('span', {'data-bind':"markupText:'currentPriceBeforePoint'"}).text)))
                try:
                    data['Rating'] = float(soup.find('span', {'class':"rating-star"}).text[:-18].replace(',', '.'))
                except AttributeError:
                    data['Rating'] = -1
                data['Ram'] = int(''.join(list(filter(lambda x: x.isdigit(), temp[temp.find("GB")-5:temp.find("GB")]))))
                data['ScreenSize'] = float(''.join(list(filter(lambda x: x.isdigit() or x == ',', temp[temp.find("inç")-6:temp.find("inç")]))).replace(',', '.'))
                data['SiteName'] = "HepsiBurada"
                data['Url'] = url
#                print(data)
                items.append(data)
    return items


# N11 sitesi scraping fonksiyonu
def N11_digger(base_url, headers):
    items = []
    for i in range(1, 1+max_page_number):   # page number range
        response = requests.get(base_url + '&page={0}'.format(i), headers=headers)      # data for a page

        soup = BeautifulSoup(response.content, 'html.parser')
        results = soup.find_all('div', attrs={'class':'catalogView ', 'class':'columnContent', 'class':'pro'})
        
        for result in results:
            data = {}
            url = result.find('a', {'class':'plink'})['href']
            try:
                response = requests.get(url=url, headers=headers)      # data for a page
            except requests.exceptions.ConnectionError:
                sleep(5)

            soup = BeautifulSoup(response.content, 'html.parser')
            temp = str(soup.find('div', {'class':'unf-prop-context'}))

            try:
                data['Title'] = soup.find('h1', {'class':'proName'}).text[22:-13]
            except AttributeError:
                data['Title'] = "Empty"
            data['Price'] = int(''.join(list(filter(lambda x: x.isdigit(), soup.find('div', {'class':'unf-p-summary-price'}).text[:-3]))))
            data['Rating'] = float(soup.find('strong', {'class':"ratingScore"}).text.replace(',', '.'))
            try:
                data['Ram'] = int(''.join(list(filter(lambda x: x.isdigit(), temp[temp.find("GB")-5:temp.find("GB")]))))
            except ValueError:
                data['Ram'] = -1
            data['ScreenSize'] = float(''.join(list(filter(lambda x: x.isdigit() or x == '.', temp[temp.find("\"<")-6:temp.find("\"<")]))))
            data['SiteName'] = "N11"
            data['Url'] = url
#            print(data)
            items.append(data)
    return items


# trendyol sitesi scraping fonksiyonu
def Trendyol_digger(base_url, headers):
    items = []
    for i in range(1, 1+max_page_number):   # page number range
        response = requests.get(base_url + '&pi={0}'.format(i), headers=headers)      # data for a page

        soup = BeautifulSoup(response.content, 'html.parser')
        results = soup.find_all('div', attrs={'class':'p-card-chldrn-cntnr card-border'})
        for result in results:
            data = {}

            temp = str(result)
            temp = temp[temp.find('href')+6:]
            temp = temp[:temp.find("\"")]

            url = "https://www.trendyol.com"+temp
            try:
                response = requests.get(url=url, headers=headers)      # data for a page
            except requests.exceptions.ConnectionError:
                sleep(5)
            soup = BeautifulSoup(response.content, 'html.parser')
            temp = str(soup.find('ul', {'class':'detail-attr-container'}))

            try:
                data['Title'] = soup.find('h1', {'class':'pr-new-br'}).text[:-1]
            except AttributeError:
                data['Title'] = "Empty"
            data['Price'] = int(''.join(list(filter(lambda x: x.isdigit(), soup.find('span', {'class':'prc-dsc'}).text[:-3].split(',')[0]))))
            data['Rating'] = soup.find('span', {'class':'tltp-avg-cnt'})
            if data['Rating'] == None:
                data['Rating'] = -1
            else:
                data['Rating'] = float(data['Rating'])
            data['Ram'] = int(''.join(list(filter(lambda x: x.isdigit(), temp.split("GB")[1][-3:-1]))))
            if data['Ram'] == 0:
                data['Ram'] = -1
            data['ScreenSize'] = float(''.join(list(filter(lambda x: x.isdigit() or x == ',', temp[temp.find("inç")-6:temp.find("inç")]))).replace(',', '.'))
            data['SiteName'] = "Trendyol"
            data['Url'] = url

            items.append(data)
#            print(data)
    return items


# scraping icin driver fonksiyonu
def scraper():
    search_query = 'laptop'.replace(' ', '+')
    items = HepsiBurada_digger('https://www.hepsiburada.com/ara?q={0}'.format(search_query), headers) + N11_digger('https://www.n11.com/arama?q={0}'.format(search_query), headers) + Trendyol_digger('https://www.trendyol.com/sr?q={0}'.format(search_query), headers)
    for item in items:
        add_item_to_db(item)










# def Amazon_digger(base_url, headers):
#     items = []

#     max_page_number = 1
#     for i in range(1, 1+max_page_number):   # page number range
#         response = requests.get(base_url, headers=HEADERS)      # data for a page
#         soup = BeautifulSoup(response.content, 'lxml')
#         results = soup.find_all('a', attrs={'class':'a-link-normal s-no-outline'})

#         for result in results:
#             if result['href'][:3] == '/gp' or result['href'][:3] == '/ss':
#                 continue
#             data = {}
#             url = "https://www.amazon.com.tr"+result['href']
#             print(url)

#             try:
#                 response = requests.get(url=url, headers=headers)      # data for a page
#             except requests.exceptions.ConnectionError:
#                 sleep(5)

#             soup = BeautifulSoup(response.content, 'html.parser')
#             data['Title'] = soup.find('span', {'id':'productTitle'}).text[8:-7]
#             try:
#                 data['Price'] = soup.find('span', {'class':'a-price-whole'}).text+soup.find('span', {'class':'a-price-symbol'}).text
#             except AttributeError:
#                 data['Price'] = "Empty"
#             print(data)
#             items.append(data)
#     return items