# -*- coding:UTF-8 -*-
# done by Yingying Wang & Keqiang Yan
import requests
from bs4 import BeautifulSoup

# import sys
# from PyQt5.QtWebEngineWidgets import QWebEnginePage as QWebPage
# from PyQt5.QtWidgets import QApplication
# from PyQt5.QtCore import QUrl
# import re


# class Render(QWebPage):
#     def __init__(self,url):
#         self.app = QApplication(sys.argv)
#         QWebPage.__init__(self)
#         self.html = ''
#         self.loadFinished.connect(self._on_load_finished)
#         self.load(QUrl(url))
#         self.app.exec_()
#     def _on_load_finished(self):
#         self.html = self.toHtml(self.Callable)
#         print('Load finished')
#         # self.app.quit()

#     def Callable(self, html_str):
#         self.html = html_str
#         self.app.quit()

class Spider(object):
    def __init__(self):
        return
    '''
    Extract html from url and find the price contained div
    Parameters: url - (string); class_name - (string)
    Return: html - (string)
    
    input example:
    eg.
        url ='https://www.podsupplies.com/products/kids-mask'

    eg. 
        the price containd <div></dic> is <div class="price__sale">...</div>
        the corresponding div_class_name is:
        div_class_name = 'price__sale'
    '''
    def get_price_div(self, url, div_class_name):
        req = requests.get(url)
        html = req.text
        div_bf = BeautifulSoup(html,features="lxml")
        # class_name = 'price__sale'
        texts = div_bf.find_all('div', class_=div_class_name)
        return str(texts)
    
    def get_price_id(self, url, div_id_name):
        req = requests.get(url)
        html = req.text
        div_bf = BeautifulSoup(html,features="lxml")
        texts = div_bf.find_all('div', id=div_id_name)
        return str(texts)
    '''
    Extract price from price contained div
    Parameters: div_bf - (string); class_name - (string)
    Return: price - (string)

    div_bf --> get from get_price_div function
    class_name can be found in <span>...</span> section which contains price
    eg.
        the price contained <span>...</span> section is
        <span class="price-item price-item--sale" data-sale-price> $9.99 </span> = $0
        so the class_name is:
        class_name = 'price-item price-item--sale'
    '''
    def get_price(self, div_bf, class_name, div_tag):
        price_bf = BeautifulSoup(div_bf,features="lxml")
        price = str(price_bf.find(div_tag, {'class' : class_name}).string)
        return price

    def abstract_price(self, url):

        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36', "Upgrade-Insecure-Requests": "1","DNT": "1","Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language": "en-US,en;q=0.5","Accept-Encoding": "gzip, deflate"}
        req = requests.get(url, headers=headers)
        
        # modify each if/elif to abstract price -- Siqi

        #Pod
        if url == 'https://www.podsupplies.com/products/kids-mask?variant=37609154871491':
            url = 'https://www.podsupplies.com/products/kids-mask?variant=37609154871491'
            s_div_name = 'price__sale'
            # o_div_name = 'price__regular'
            sale_span_name = 'price-item price-item--sale'
            # orig_span_name = 'price-item price-item--regular'
            s_div = self.get_price_div(url, s_div_name)
            sale_price = self.get_price(s_div, sale_span_name,'span').strip()

        #Wayre
        elif url == 'https://www.shopwayre.com/collections/all/products/kids-high-tech-washable-mask':
            # There are many prices in this page, I choose only one from them -- Siqi
            # soup = BeautifulSoup(req.text, 'html.parser')
            # texts = soup.find('meta', property='product:price:amount')
            # sale_price = '$'+texts["content"]
            url = 'https://www.shopwayre.com/collections/all/products/kids-high-tech-washable-mask'
            s_div_name = "ProductMeta__PriceList Heading"  
            sale_span_name = "ProductMeta__Price Price Price--highlight Text--subdued u-h4"
            s_div = self.get_price_div(url, s_div_name)
            sale_price = self.get_price(s_div, sale_span_name,'span').strip()


        # Happy Mask 
        elif url == 'https://www.happymasks.com/collections/pro/products/black-pro':
            url = 'https://www.happymasks.com/collections/pro/products/black-pro'
            s_div_name = 'price-container'
            sale_span_name = 'product-single__price'
            s_div = self.get_price_div(url, s_div_name)
            sale_price = self.get_price(s_div, sale_span_name,'span').strip()
        
        #Honeywell 
        elif url == 'https://ppe.honeywell.com/collections/face-covers/products/honeywell-3d-knit-face-mask-light-grey-size-s-m-4-pk':
            url = 'https://ppe.honeywell.com/collections/face-covers/products/honeywell-3d-knit-face-mask-light-grey-size-s-m-4-pk'
            s_div_name = 'product-price--mobile'
            # sale_span_name = 'money bfx-price'
            sale_span_name = 'money'
            # s_div = self.get_price_div(url, s_div_name)
            s_div = self.get_price_id(url, s_div_name)

            price_bf = BeautifulSoup(s_div,features="lxml")
            price = str(price_bf.find('span', {'class' : 'onsale'}))

            sale_price = self.get_price(price, sale_span_name,'span').strip()

        #Caraa
        elif url == 'https://caraasport.com/products/3-tailored-junior-masks?variant=39513097764944':
            url = 'https://caraasport.com/products/3-tailored-junior-masks?variant=39513097764944'
            s_div_name = 'price-flex'
            sale_span_name = 'f4-l f3-ns f4 ttu gold tracked brandon'
            s_div = self.get_price_div(url, s_div_name)
            # sale_price = self.get_price(s_div, sale_span_name,'span').strip()
            price_bf = BeautifulSoup(s_div, features="lxml")
            price = str(price_bf.find('span', {'id' : "ProductPrice"})['content'])

            price_bf = BeautifulSoup(price, features="lxml")
            price = str(price_bf.find('span', {'class' : 'money'}).string)
            sale_price = price.strip()

        #Flomask 
        elif url == 'https://flomask.com/collections/flo-mask-bundle-mask-12-filters/products/flo-mask-essential-bundle':
            url = 'https://flomask.com/collections/flo-mask-bundle-mask-12-filters/products/flo-mask-essential-bundle'
            s_div_name = "price__regular"
            sale_span_name = "price-item price-item--regular"
            s_div = self.get_price_div(url, s_div_name)
            sale_price = self.get_price(s_div, sale_span_name,'span').strip()
        
        # 3M
        elif url == 'https://www.3m.com/3M/en_US/p/d/v000075539/':
            url = 'https://www.3m.com/3M/en_US/p/d/v000075539/'
            #########################################################################
            # 3M is somehow special with JavaScript price part, we tried following methods
            # but not succeed, propbably multi-thread Render can help
            #########################################################################
            # s_div_name = "mkpl-price"
            # sale_span_name = "mkpl-price_value"
            # s_div = self.get_price_div(url, s_div_name)
            # html = req.text
            # div_bf = BeautifulSoup(html, features="lxml")
            # texts = div_bf.find_all('div', class_="MMM--selectionBox--cntnr")
            # print(texts)
            # sale_price = self.get_price(s_div, sale_span_name,'span').strip()

            sale_price = "$0"
            
            # page = Render(url)
            # html = BeautifulSoup(page.html, 'html.parser')
            # price_bf = html.find('p', class_='mkpl-price_value')
            # print(html)
            # print("????")
            # print(price_bf.text)
            # sale_price = re.findall(r"(\$[0-9]+\.*[0-9]*)", price_bf.text)[0]

        else:
            sale_price = "$0"
        print(sale_price)
        print(url)
        return sale_price
  
    
    
