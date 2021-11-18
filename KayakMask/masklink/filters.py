import django_filters

from .models import MaskInfo

class MaskFilter(django_filters.FilterSet): 

    class Meta: 
        model = MaskInfo
        fields = [
            'size', 
            'available',
            'brand'
        ]
