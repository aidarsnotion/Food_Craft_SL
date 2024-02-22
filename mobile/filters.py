import django_filters
from main.models import *

class ProductsFilter(django_filters.FilterSet):
    language = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Products
        fields = ['id', 'language', 'attribute_name', 'Category']