import django_filters
from django_filters import DateFilter,CharFilter
from django_filters import parse_version
from .models import *

class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='date_created',lookup_expr='gte',label='التاريخ يبدأ ب')
    end_date = DateFilter(field_name='date_created',lookup_expr='lte',label='التاريخ ينتهي ب')
    note = CharFilter(field_name='note',lookup_expr='icontains')

    
    class Meta:
        model=Order
        fields = '__all__'
        exclude = ['customer','date_created']
        
    
