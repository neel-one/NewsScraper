from bs4 import BeautifulSoup
import requests
import pandas as pd
"""
NewsScraper is a library that supports article and title scraping for multiple news sites. Although most parts of scraping
news articles and titles are the same, each site has different methods. Therefore, to add support, simply add another class
that extends the base class and override the NotImplemented methods in the abstract base class.
TODO: implement errorr handling, add support for more sites, find away to bypass IP blocks when scraping too many articles,
'&amp -> &'
"""
class Scraper(object):
    def __init__(self, limit = 60, page = 1):
        self.limit = limit
        self.page = page

    def update_api(self):
        raise NotImplementedError("This is an abstract class!")

    def edit(self, y):
        g = ""
        record = False
        for i in y:
            if(i == '<'):
                record = False
            if(record):
                g+=i
            if(i == '>'):
                record = True
        g = g.lstrip()
        return g

    def find_titles_on_page(self, soup):
        raise NotImplementedError("This is an abstract class!")

    def find_titles(self):
        soup = self.update_api()
        amount = 0
        title_list = []
        date_list = []
        while(amount < self.limit):
            titles,dates = self.find_titles_on_page(soup)
            title_list += titles
            date_list += dates
            self.page+=1
            print("Scraping next page... Page: " + str(self.page) + " Titles: " + str(len(title_list)))
            #Reload API for next page
            soup = self.update_api()
            amount = len(title_list)
            if(len(titles) == 0):
                amount = self.limit
        print('Done!')
        return title_list,date_list

    def save_csv(self,df,filename):
        with open(filename, 'a+') as f:
            df.to_csv(f, header=False)

class CNBCScraper(Scraper):
    def __init__(self, limit = 60, page = 1):
        super().__init__(limit,page)
    def update_api(self):
        url = "https://www.cnbc.com/trading-nation/?page="
        url += str(self.page)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
        response = requests.get(url, headers = headers)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup
    def find_titles_on_page(self, soup):
        title_list = []
        date_list = []
        x = soup.find_all(class_ = "Card-titleContainer",limit=60)
        y = soup.find_all(class_ = "Card-time",limit=60)
        for i,j in zip(x,y):
            title = i.find(title="")
            titles = self.edit(str(title))
            date = self.edit(str(j))
            title_list.append(titles)
            date_list.append(date)
            print(date)
            print(titles)
        return title_list,date_list

class ReutersScraper(Scraper):
    def __init__(self, limit = 60, page = 1):
        super().__init__(limit,page)
    def update_api(self):
        url = "https://www.reuters.com/news/archive/businessNews/"
        if(self.page > 1):
            url = "https://www.reuters.com/news/archive/businessNews/?view=page&page=" + str(self.page) +"&pageSize=10"
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
        response = requests.get(url, headers = headers)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup
    
    def find_titles_on_page(self, soup):
        title_list = []
        date_list = []
        x = soup.find_all(class_ = "story-title",limit=60)
        y = soup.find_all(class_ = "timestamp",limit=60)
        for i,j in zip(x,y):
            titles = self.edit(str(i))
            date = self.edit(str(j))
            title_list.append(titles)
            date_list.append(date)
            print(date)
            print(titles)
        return title_list,date_list

class SeekingAlphaScraper(Scraper):
    def __init__(self, limit = 60, page = 1):
        super().__init__(limit,page)

    def update_api(self):
        url = "https://seekingalpha.com/market-news/"
        url += str(self.page)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
        response = requests.get(url, headers = headers)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup
    
    def find_titles_on_page(self, soup):
        title_list = []
        date_list = []
        x = soup.find_all(class_ = "add-source-assigned",limit=60)
        y = soup.find_all(class_ = "item-date",limit=60)
        for i,j in zip(x,y):
            titles = self.edit(str(i))
            date = self.edit(str(j))
            title_list.append(titles)
            date_list.append(date)
            print(date)
            print(titles)
        return title_list,date_list

class FinancialTimesScraper(Scraper):
    def __init__(self, limit = 60, page = 1):
        super().__init__(limit,page)

    def update_api(self):
        url = "https://www.ft.com/markets?page="
        url += str(self.page)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
        response = requests.get(url, headers = headers)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup
    
    def find_titles_on_page(self, soup):
        title_list = []
        date_list = []
        x = soup.find_all(class_ = "js-teaser-heading-link",limit=60)
        #y = soup.find_all(class_ = "item-date",limit=60)
        for i in x:
            titles = self.edit(str(i))
            date = "NA"
            title_list.append(titles)
            date_list.append(date)
            print(titles)
        return title_list,date_list
class WSJScraper(Scraper):
    def __init__(self, limit = 60, page = 1, year = 2019, month = 11, day = 14):
        super().__init__(limit,page)
        self.year = year
        self.month = month
        self.day = day
    def update_day(self):
        if(self.day != 0):
            self.day -= 1
        else:
            self.month -= 1
            if(self.month == 4 or self.month == 6 or self.month == 9 or  self.month == 11):
                self.day = 30
            elif(self.month == 2):
                self.day = 28
            elif(self.month == 0):
                self.year -= 1
                self.month = 12
                self.day = 31
            else:
                self.day = 31
    def update_api(self):
        url = "https://www.wsj.com/news/archive/"
        url += str(self.year)
        url += str(self.month)
        url += str(self.day)
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
        response = requests.get(url, headers = headers)
        soup = BeautifulSoup(response.content, "html.parser")
        return soup
    def edit(self, y):
        g = ""
        quote = 0
        for i in y:
            if(i == '\"' and quote == 1):
                break
            if(quote == 1):
                g+=i
            if(i == '\"'):
                quote += 1
        return g
    
    def find_titles_on_page(self, soup):
        title_list = []
        date_list = []
        x = soup.find_all(class_="WSJTheme--image--38W4jSen",limit=150)
        for i in x:
            titles = self.edit(str(i))
            date = str(self.month) + "/" + str(self.day) + "/" + str(self.year)
            title_list.append(titles)
            date_list.append(date)
            print(titles)
            print(date)
        return title_list,date_list
    def find_titles(self):
        #page = 1
        #inits the api to page 1 of trading nation
        soup = self.update_api()
        amount = 0
        title_list = []
        date_list = []
        while(amount < self.limit):
            titles,dates = self.find_titles_on_page(soup)
            title_list += titles
            date_list += dates
            self.page+=1
            print("Scraping next page... Page: " + str(self.page) + " Titles: " + str(len(title_list)))
            #Reload API for next page
            self.update_day()
            soup = self.update_api()
            amount = len(title_list)
            if(len(titles) == 0):
                amount = self.limit
        print('Done!')
        return title_list,date_list

