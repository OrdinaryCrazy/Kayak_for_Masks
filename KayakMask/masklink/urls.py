from django.urls import path
# from . import views
from masklink.views import MaskIndex, MaskSpider

app_name = 'masklink'

urlpatterns = [
    path('', MaskIndex, name="mask_index"),
    path('spider/', MaskSpider, name="mask_spider"),
]