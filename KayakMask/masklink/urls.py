from django.urls import path
from . import views

app_name = 'masklink'

urlpatterns = [
    path('', views.MaskIndex, name="mask_index"),
    path('spider/', views.MaskSpider, name="mask_spider"),
]