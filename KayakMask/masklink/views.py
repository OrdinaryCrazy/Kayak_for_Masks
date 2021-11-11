import re

from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse 

from .forms import MaskChoiceForm
from .models import MaskInfo
#
from .filters import MaskFilter
#
import pygsheets

#Filter 
def show_all_mask_page(request):

    context = {}

    filtered_masks = MaskFilter(
        request.GET,
        queryset=MaskInfo.objects.all()
    )

    context['filtered_masks'] = filtered_masks.qs 

    return render(request, 'masklink/index.html' , context = context)
#
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
        google_client = pygsheets.authorize(service_file=r"C:\Users\13025\Desktop\CSCE606\Kayak_for_Masks\KayakMask\masklink\astute-being-331516-f44fa7b84e38.json")
        sheets = google_client.open_by_url(
            # 'https://docs.google.com/spreadsheets/d/17HEwAGxVkFrqZM6hSorVJHUHI7gyQjBagGszc4I5VLw/'
            'https://docs.google.com/spreadsheets/d/17HEwAGxVkFrqZM6hSorVJHUHI7gyQjBagGszc4I5VLw/edit#gid=15734172'
        )
        self.mask_sheet = sheets[1].get_as_df()
        # print(self.mask_sheet)
        # for col in self.mask_sheet.columns:
        #     print('column name: ', col)
        #     print(len(col))
        self.data = []
    
    def spider_all_items(self):
        # print(self.mask_sheet["Type of mask"])
        # print('[spider_all_items]')
        # for col in self.mask_sheet.columns:
        #     print('column name: ', col)
        
        # for i, mask in enumerate(self.mask_sheet,):
        for i in range(7):
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
            item_model.save()

# if __name__ == "__main__":
#     spider = MaskLinkSpider(None)
