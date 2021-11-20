from django import forms
from django.forms.forms import Form
from django.test import TestCase
from django.db import models
from masklink.models import MaskInfo
from django.urls.conf import _path,path
from functools import partial
from django.urls.resolvers import RoutePattern
from masklink.views import MaskIndex, MaskSpider, MaskChoiceForm
from .urls import urlpatterns
# Create your tests here.

#Test cases for the mask list display
class MaskTitleTestCase(TestCase):
    def TitleSetup(self):
        MaskInfo.object.create(name="name")
        MaskInfo.object.create(brand="brand")
        MaskInfo.object.create(size="size")
        MaskInfo.object.create(link="link")
        MaskInfo.object.create(link="fe")
    def test_Mask_info(self):
        name = models.CharField(verbose_name="name")
        brand = models.CharField(verbose_name="brand")
        size = models.CharField(verbose_name="size")
        link = models.CharField(verbose_name="purchasing link")
        fe = models.CharField(verbose_name="filtration efficiency")

#Test cases for clicking purchase link
class MaskLinkTestCase(TestCase):
    def Linksetup(self):
        path = partial(_path, Pattern=RoutePattern)
        urlpatterns = [
            path('', MaskIndex, name="mask_index"),
            path('spider/', MaskSpider, name="mask_spider"),
        ]
    def test_Link(self):
        path.click = urlpatterns

#Test cases for 
class SortingTestCase(TestCase):
    def SortingSetUp(self, request, form):
        MaskChoiceForm.form.data = request.POST or None
        form = MaskChoiceForm.form.data
    
    def test_Sorting(form):
        if form == "size":
            form.mask_sheet.sort_values('Size', ascending=False, inplace=True)
        elif form == "filtration":
            form.mask_sheet.sort_values('Claimed filtration efficiency', ascending=False, inplace=True)
        elif form == "name":
            form.mask_sheet.sort_values('Type of mask', inplace=True)
        # Sorting end

#FilterTest(one example)
class FilterTestCase(TestCase):
    def FilterSetup(self, request, mask_sheet):
        MaskChoiceForm.mask_sheet = request.POST or None
        mask_sheet = MaskChoiceForm.mask_sheet
    def test_Filter(mask_sheet):
        if mask_sheet == "small":
            mask_sheet = mask_sheet[(mask_sheet['Size']=='Small')]

#availabilityTest
class availabilityTestCase(TestCase):
    def avaSetup(self, request, form, index, mask_sheet, avaStat):
        MaskChoiceForm.form.data = request.POST or None
        index = MaskChoiceForm.form.mask_sheet.index
        mask_sheet = MaskChoiceForm.form.mask_sheet
        form = MaskChoiceForm.form.data.mask_sheet.drop(index[mask_sheet['avai'].data])

    def test_Ava(form):
        if form == "1":
            form['Availablity']=='No'
        elif form  == '0':
            form['Availablity']=='Yes'