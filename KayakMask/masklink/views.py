import re

from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse 

from .forms import MaskChoiceForm
from .models import MaskInfo
from .spider_1206 import Spider

import pygsheets

#Filter
def show_all_mask_page(request):

    context = {}
    print("here")
    filtered_masks = MaskFilter(
        request.GET,
        queryset=MaskInfo.objects.all()
    )

    context['filtered_masks'] = filtered_masks.qs 

    return render(request, 'masklink/index.html' , context = context)

# Create your views here.
def MaskIndex(request):
    form = MaskChoiceForm()
    maskList = MaskInfo.objects.all()
    if maskList:
        paginator = Paginator(maskList, 100)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)
        return render(request, 'masklink/index.html', 
                    {
                        'page_obj': page_obj,
                        'paginator': paginator,
                        'is_paginated': True, 
                        'form': form,
                    })
    
    else:
        return render(request,'masklink/index.html', 
                    {
                        'form': form,
                    })


def MaskSpider(request):
    if request.method == "POST":
        form = MaskChoiceForm(data = request.POST or None)
        print(form.is_valid)
        if form.is_valid:
            # url = form.cleaned_data.get('brand')
            spider = MaskLinkSpider(form)
            spider.spider_all_items()
            spider.save_data_to_model()
            return HttpResponseRedirect('/masklink/')
        else:
            print("GGG")
            print(form.errors)
            spider = MaskLinkSpider(form)
            return HttpResponseRedirect('/masklink/')
    else:
        return HttpResponseRedirect('/masklink/')

class MaskLinkSpider(object):
    def __init__(self, form) -> None:
        super().__init__()
        self.form = form
        google_client = pygsheets.authorize(service_file=r"./masklink/astute-being-331516-f44fa7b84e38.json")
        sheets = google_client.open_by_url(
            # 'https://docs.google.com/spreadsheets/d/17HEwAGxVkFrqZM6hSorVJHUHI7gyQjBagGszc4I5VLw/'
            'https://docs.google.com/spreadsheets/d/17HEwAGxVkFrqZM6hSorVJHUHI7gyQjBagGszc4I5VLw/edit#gid=15734172'
        )
        self.mask_sheet = sheets[1].get_as_df()
        print(self.mask_sheet)
        # will return a list
        print(self.form["brand"].data)

        for col in self.mask_sheet.columns:
            print('column name: ', col)
            print(len(col))

        # Obtain current price
        for ind in range (len(self.mask_sheet['shoppingLink'])):
            print(type(self.mask_sheet['Cost per mask']))
            self.mask_sheet.at[ind,'Cost per mask'] = Spider().abstract_price(self.mask_sheet['shoppingLink'][ind])

        # Sorting -- Siqi
        if self.form['sorting'].data == "size":
            self.mask_sheet.sort_values('Size', ascending=False, inplace=True)
        elif self.form['sorting'].data == "filtration":
            self.mask_sheet.sort_values('Claimed filtration efficiency', ascending=False, inplace=True)
        elif self.form['sorting'].data == "name":
            self.mask_sheet.sort_values('Type of mask', inplace=True)
        # Sorting end

        # Single-Size Filtering Starts -- Hanzhou
        '''
        if self.form['size'].data == "small":
            # In the goole form, 'Medium' might be 'Medium ', 'Medium  ' and etc (with multiple spaces). 
            # So we handle 'Small' instead of 'Medium'.
            self.mask_sheet = self.mask_sheet[(self.mask_sheet['Size']=='Small')]
        elif self.form['size'].data == 'mid':
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Size']=='Small'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Size']=='OneSize'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Size']=='XS: 4.7x5.3 inch (Toddler, Valveless, Non-Adjustable)'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Size']=='M: 5.9x7.5 inch'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Size']=='S: 5.5x6.7 inch'], inplace=True)
        
        # Add More Filtering Items (Size) -- Yuncheng 
        
        elif self.form['size'].data == 'onesize':
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Size']=='Small'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Size']=='XS: 4.7x5.3 inch (Toddler, Valveless, Non-Adjustable)'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Size']=='M: 5.9x7.5 inch'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Size']=='S: 5.5x6.7 inch'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Size']=='Medium'], inplace=True)
        elif self.form['size'].data == 'XS':
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Size']=='Small'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Size']=='Medium'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Size']=='M: 5.9x7.5 inch'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Size']=='S: 5.5x6.7 inch'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Size']=='OneSize'], inplace=True)
        elif self.form['size'].data == 'S':
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Size']=='Small'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Size']=='Medium'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Size']=='XS: 4.7x5.3 inch (Toddler, Valveless, Non-Adjustable)'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Size']=='M: 5.9x7.5 inch'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Size']=='OneSize'], inplace=True)
        elif self.form['size'].data == 'M':
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Size']=='Small'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Size']=='Medium'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Size']=='OneSize'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Size']=='XS: 4.7x5.3 inch (Toddler, Valveless, Non-Adjustable)'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Size']=='S: 5.5x6.7 inch'], inplace=True)
        '''
        # Single-Size Filtering Ends
        
        # Single-Brand Filtering Starts -- Yuncheng 
        '''
        if self.form['brand'].data == "3m_vflex":
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='POD'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Happy Mask'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Flomask'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Cambridge'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Caraa Tailored Junior Mask'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Honeywell'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Wayre'], inplace=True)

        elif self.form['brand'].data == 'pod':
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Happy Mask'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Flomask'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Cambridge'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Caraa Tailored Junior Mask'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Honeywell'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Wayre'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='3M Vflex'], inplace=True)

        elif self.form['brand'].data == 'happy_mask':
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='POD'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Flomask'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Cambridge'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Caraa Tailored Junior Mask'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Honeywell'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Wayre'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='3M Vflex'], inplace=True)

        elif self.form['brand'].data == 'flo_mask':
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Happy Mask'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='POD'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Cambridge'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Caraa Tailored Junior Mask'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Honeywell'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Wayre'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='3M Vflex'], inplace=True)

        elif self.form['brand'].data == 'wayre':
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Happy Mask'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Flomask'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Cambridge'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Caraa Tailored Junior Mask'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Honeywell'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='POD'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='3M Vflex'], inplace=True)
        
        elif self.form['brand'].data == 'carra':
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Happy Mask'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Flomask'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Cambridge'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='POD'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Honeywell'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Wayre'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='3M Vflex'], inplace=True)
        
        elif self.form['brand'].data == 'cambridge':
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Happy Mask'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Flomask'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='POD'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Caraa Tailored Junior Mask'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Honeywell'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Wayre'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='3M Vflex'], inplace=True)
        
        elif self.form['brand'].data == 'honeywell':
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Happy Mask'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Flomask'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Cambridge'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Caraa Tailored Junior Mask'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='POD'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='Wayre'], inplace=True)
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']=='3M Vflex'], inplace=True)
        '''
        # Single-Brand Filtering Ends
        

        # Multi-Size Filtering Starts
        print('form brand column data =', self.form['size'].data)

        size_list_low = ['small', 'mid', 'onesize', 'XS', 'M', 'S']
        size_list_up = ['Small', 'Medium', 'Onesize', 'XS', 'M', 'S']

        rmv_size_list = list(set(size_list_low)-set(self.form['size'].data))
        for size_low in rmv_size_list:
            size_list_index = size_list_low.index(size_low)
            size_up = size_list_up[size_list_index]
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Size']==size_up], inplace=True)

        # Multi-Size Filtering Ends

        # Multi-Brand Filter Starts
        print('form brand column data =', self.form['brand'].data)

        brand_list_low = ['3m_vflex', 'pod', 'happy_mask', 'flo_mask', 'wayre', 'carra', 'cambridge', 'honeywell']
        brand_list_up =  ['3M Vflex', 'POD', 'Happy Mask', 'Flomask', 'Wayre', 'Caraa Tailored Junior Mask', 'Cambridge', 'Honeywell']
        
        rmv_brand_list = list(set(brand_list_low)-set(self.form['brand'].data))

        for brand_low in rmv_brand_list:
            brand_list_index = brand_list_low.index(brand_low)
            brand_up = brand_list_up[brand_list_index]
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Brand']==brand_up], inplace=True)
        # Multi-Brand Filter Ends


        # elif self.form['Brand/Manufacture'].data == 'happy_mask':
        #     self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Availablity']=='Yes'], inplace=True)
        # elif self.form['Brand/Manufacture'].data == 'flo_mask':
        #     self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Availablity']=='Yes'], inplace=True)
        # elif self.form['Brand/Manufacture'].data == 'wayre':
        #     self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Availablity']=='Yes'], inplace=True)
        # elif self.form['Brand/Manufacture'].data == 'carra':
        #     self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Availablity']=='Yes'], inplace=True)
        # elif self.form['Brand/Manufacture'].data == 'cambridge':
        #     self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Availablity']=='Yes'], inplace=True)
        # elif self.form['Brand/Manufacture'].data == 'honeywell':
        #     self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Availablity']=='Yes'], inplace=True)
        
        
        # Filtering end
    #######################################################################

        if self.form['avai'].data == "1":
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Availablity']=='No'], inplace=True)
        elif self.form['avai'].data == '0':
            self.mask_sheet.drop(self.mask_sheet.index[self.mask_sheet['Availablity']=='Yes'], inplace=True)
        # Filtering end

        # print(self.mask_sheet)
        self.mask_sheet.reset_index(drop=True, inplace=True) # generate new sequential index
        self.data = []
    
    def spider_all_items(self):
        # print(self.mask_sheet["Type of mask"])
        # print('[spider_all_items]')
        # for col in self.mask_sheet.columns:
        #     print('column name: ', col)
        
        # for i, mask in enumerate(self.mask_sheet,):
        # self.mask_sheet.shape[0] is the dynamic depth of the form.
        for i in range(self.mask_sheet.shape[0]):
            mask_attribute = {}
            mask_attribute['name'] = self.mask_sheet["Type of mask"][i]
            mask_attribute['brand'] = self.mask_sheet["Brand"][i]
            
            # print(mask_attribute['brand'])
            mask_attribute['size'] = self.mask_sheet["Size"][i]
            
            # print(mask_attribute['size'])
            mask_attribute['price'] = float(re.findall(r"\$([0-9]+\.*[0-9]*)", self.mask_sheet["Cost per mask"][i])[0])
            mask_attribute['available'] = self.mask_sheet["Availablity"][i]
            mask_attribute['link'] = self.mask_sheet["shoppingLink"][i]
            mask_attribute['fe'] = float(max([
                                    sorted(re.findall(r"([0-9]+\.*[0-9]*)\%", 
                                        self.mask_sheet["Claimed filtration efficiency"][i]), reverse=True),
                                    sorted(re.findall(r"([0-9]+\.*[0-9]*)\%", 
                                        self.mask_sheet["Independent testing results"][i]), reverse=True),
                                    sorted(re.findall(r"([0-9]+\.*[0-9]*)\%", 
                                        self.mask_sheet["Our results, as worn on kids"][i]), reverse=True),
                                ])[0])

            
            self.data.append(mask_attribute)
            

    def save_data_to_model(self):
        MaskInfo.objects.all().delete()
        for item in self.data:
            item_model = MaskInfo()
            item_model.name = item['name']
            item_model.brand = item['brand']
            item_model.size = item['size']
            item_model.price = item['price']
            item_model.available = item['available']
            item_model.link = item['link']
            item_model.fe = item['fe']
            # item_model.time = item['time']
            item_model.save()

# if __name__ == "__main__":
#     spider = MaskLinkSpider(None)
