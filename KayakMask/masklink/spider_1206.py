# -*- coding:UTF-8 -*-
# done by Yingying Wang & Keqiang Yan
import requests
from bs4 import BeautifulSoup

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
        if url == 'https://www.podsupplies.com/products/kids-mask':
            url = 'https://www.podsupplies.com/products/kids-mask'
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
            s_div_name = 'product-price'
            sale_span_name = 'money bfx-price'
            s_div = self.get_price_div(url, s_div_name)
            sale_price = self.get_price(s_div, sale_span_name,'span').strip()

        #Caraa
        elif url == 'https://caraasport.com/products/3-tailored-junior-masks?variant=39513097764944':
            url = 'https://caraasport.com/products/3-tailored-junior-masks?variant=39513097764944'
            s_div_name = 'price-flex'
            sale_span_name = 'money'
            s_div = self.get_price_div(url, s_div_name)
            sale_price = self.get_price(s_div, sale_span_name,'span').strip()


        #Flomask 
        else:
            url = 'https://flomask.com/collections/flo-mask-bundle-mask-12-filters/products/flo-mask-essential-bundle'
            s_div_name = "price__regular"
            sale_span_name = "price-item price-item--regular"
            s_div = self.get_price_div(url, s_div_name)
            sale_price = self.get_price(s_div, sale_span_name,'span').strip()
        print(sale_price)
        return sale_price
  
    
    
