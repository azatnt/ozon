from django.urls import path
from .views import *

urlpatterns = [
    path('', GetProductList.as_view(), name='get_product_by_status_url'),
    path('archive_product/<int:id>', ArchiveProduct.as_view(), name='archive_product_url'),
    path('archived_products', ArchivedProducts.as_view(), name='archive_list_url')
]
