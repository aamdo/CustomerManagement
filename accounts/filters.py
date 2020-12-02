import django_filters
from django_filters import parse_version
from .models import *

class OrderFilter(django_filters.FilterSet):
    class Meta:
        model=Order
        fields = '__all__'
    
