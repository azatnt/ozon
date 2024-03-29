from django.urls import path
from .views import *

urlpatterns = [
    path('', Home.as_view(), name='home_urls'),
    path('products_list/by_warehouse/<int:id>', GetProductList.as_view(), name='get_products_url'),
    path('check_warehouse', CheckWarehouse.as_view(), name='check_warehouse_url'),
    path('archive_product/<int:id>/<int:warehouse_id>', ArchiveProduct.as_view(), name='archive_product_url'),
    path('driver_product_done/<int:id>/<int:warehouse_id>', DriverProductDone.as_view(), name='driver_product_done_url'),
    path('archived_products/<int:id>', ArchivedProducts.as_view(), name='archive_list_url'),
    path('remove_from_archive/<int:id>/<int:warehouse_id>', RemoveFromArchive.as_view(), name='remove_from_archive_url'),
    path('upload_articles', UploadArticles.as_view(), name='upload_articles_urls'),
    path('products_list/by_warehouse/<int:id>/<int:warehouse_id>', ProductsForDriver.as_view(),
         name='products_list_for_driver'),
    path('manager/<int:id>/<int:warehouse_id>', Admin.as_view(), name='admin_urls'),
    path('manager_archive/<int:id>/<int:warehouse_id>', AdminArchive.as_view(), name='admin_archive_urls'),
    path('export_to_excel', ExportToExcel.as_view(), name='export_to_excel_url')
]
