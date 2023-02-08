from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home_urls'),
    path('products_list/by_warehouse/<int:id>', GetProductList.as_view(), name='get_products_url'),
    path('check_warehouse', CheckWarehouse.as_view(), name='check_warehouse_url'),
    path('archive_product/<int:id>/<int:warehouse_id>', ArchiveProduct.as_view(), name='archive_product_url'),
    path('archived_products/<int:id>', ArchivedProducts.as_view(), name='archive_list_url'),
    path('remove_from_archive/<int:id>/<int:warehouse_id>', RemoveFromArchive.as_view(), name='remove_from_archive_url'),
    path('upload_articles', UploadArticles.as_view(), name='upload_articles_urls')
]
