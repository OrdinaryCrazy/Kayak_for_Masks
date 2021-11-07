import requests

from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect

from .forms import MaskChoiceForm
from .models import MaskInfo

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
        form = MaskChoiceForm(request.POST)
    else:
        return HttpResponseRedirect('/masklink/')

class MaskLinkSpider(object):
    def __init__(self) -> None:
        super().__init__()

