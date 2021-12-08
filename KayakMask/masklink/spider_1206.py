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
# modify each if/elif to abstract price -- Yingying 
if __name__ == '__main__':
    url = 'https://www.happymasks.com/collections/pro/products/black-pro'
    # s_div_name = 'price__sale'
    o_div_name = 'price-container'
    # sale_span_name = 'price-item price-item--sale'
    orig_span_name = 'product-single__price'
    
    sp = Spider()
    # s_div = sp.get_price_div(url, s_div_name)
    # sale_price = sp.get_price(s_div, sale_span_name,'span').strip()
    
    o_div = sp.get_price_div(url, o_div_name)
    orig_price = sp.get_price(o_div, orig_span_name, 'span').strip()
    # print(sale_price, orig_price)
    print(orig_price)
  
    
    
