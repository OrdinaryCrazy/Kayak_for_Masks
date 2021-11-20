from django.test import TestCase
from django.db import models
from masklink.models import MaskInfo
from django.urls.conf import _path,path
from functools import partial
from django.urls.resolvers import RoutePattern, URLPattern
from masklink.views import MaskIndex, MaskSpider
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