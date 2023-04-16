import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.views import APIView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from pyexcel_xlsx import get_data as xlsx_get
from pyexcel_xls import get_data as xls_get


from shop.models import Product, ArticleNumber, Warehouse


class Home(APIView):
    def get(self, request):
        return render(request, 'base.html', context={})


class CheckWarehouse(APIView):
    def post(self, request, *args, **kwargs):
        param = request.POST.get('warehouse')
        warehouse = Warehouse.objects.filter(name=param).first()
        if warehouse and warehouse.id == 4:
            return redirect('products_list_for_driver', id=warehouse.id, warehouse_id=1)
        elif warehouse and warehouse.id == 5:
            return redirect('admin_urls', id=warehouse.id, warehouse_id=1)
        elif warehouse:
            return redirect('get_products_url', id=warehouse.id)
        messages.error(request, 'Склад не существует!')
        return redirect('home_urls')


class GetProductList(APIView):
    def get(self, request, id):
        queryset = Product.objects.filter(is_archive=False).filter(is_driver=False).filter(warehouse_id=id).select_related('warehouse').order_by('-date')
        warehouse_id = id
        page = request.GET.get('page', 1)
        warehouses = Warehouse.objects.exclude(id=4)
        paginator = Paginator(queryset, 10)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        return render(request, "index.html", context={"products": products, "warehouse_id": warehouse_id,
                                                      "warehouses": warehouses})


class ArchiveProduct(APIView):
    def post(self, request, id, warehouse_id):
        product = Product.objects.get(id=id)
        product.is_archive = True
        product.is_driver = True
        product.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class DriverProductDone(APIView):
    def post(self, request, id, warehouse_id):
        product = Product.objects.get(id=id)
        product.is_archive = True
        product.is_driver = False
        product.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ArchivedProducts(APIView):
    def get(self, request, id):
        products = Product.objects.filter(is_archive=True).filter(warehouse_id=id)
        warehouse_id = id
        page = request.GET.get('page', 1)
        paginator = Paginator(products, 10)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        return render(request, 'archive.html', context={"products": products, "warehouse_id": warehouse_id})


class RemoveFromArchive(APIView):
    def post(self, request, id, warehouse_id):
        product = Product.objects.get(id=id)
        product.is_archive = False
        product.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class UploadArticles(APIView):
    def post(self, request):
        warehouse_name = request.POST.get('warehouse')
        try:
            excel_file = request.FILES['file']
        except MultiValueDictKeyError:
            return redirect('home_urls')

        if str(excel_file).split('.')[-1] == "xlsx":
            data = xlsx_get(excel_file, column_limit=4)
        elif str(excel_file).split('.')[-1] == "xls":
            data = xls_get(excel_file, column_limit=4)
        else:
            return redirect('home_urls')

        value = data[list(data.keys())[0]]
        warehouse = Warehouse.objects.get(name=warehouse_name)
        for i in value:
            data = ArticleNumber.objects.filter(name=str(i[0]), warehouse=warehouse)
            if not data.exists():
                ArticleNumber.objects.create(name=str(i[0]), warehouse=warehouse)
        return redirect('home_urls')


class ProductsForDriver(APIView):
    def get(self, request, id, warehouse_id):
        warehouses = Warehouse.objects.exclude(id=id).exclude(id=5)
        products = Product.objects.filter(warehouse_id=warehouse_id).filter(is_driver=True).select_related('warehouse').order_by('date')
        page = request.GET.get('page', 1)
        paginator = Paginator(products, 10)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        return render(request, 'index.html', context={'products': products, 'warehouse_id': id, 'warehouses': warehouses})


class Admin(APIView):
    def get(self, request, id, warehouse_id):
        warehouses = Warehouse.objects.exclude(id__in=[4, 5])
        warehouse = Warehouse.objects.get(id=warehouse_id)
        products = Product.objects.filter(warehouse_id=warehouse_id, is_archive=False).select_related('warehouse').order_by('-date')
        page = request.GET.get('page', 1)
        paginator = Paginator(products, 10)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        return render(request, 'admin.html', context={'warehouses': warehouses, 'admin_id': id, 'warehouse': warehouse,
                                                      'products': products})


class AdminArchive(APIView):
    def get(self, request, id, warehouse_id):
        warehouses = Warehouse.objects.exclude(id__in=[4, 5])
        warehouse = Warehouse.objects.get(id=warehouse_id)
        products = Product.objects.filter(is_archive=True).filter(warehouse_id=warehouse_id).select_related('warehouse').order_by('-date')
        page = request.GET.get('page', 1)
        paginator = Paginator(products, 10)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        return render(request, 'admin_archive.html', context={'warehouses': warehouses, 'admin_id': id, 'warehouse': warehouse,
                                                              'products': products})


class ExportToExcel(APIView):
    def post(self, request, id):
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        params = {}
        today = datetime.datetime.today()
        if start_date is not None and end_date is not None:
            params['date__gte'] = start_date
            params['date__lte'] = end_date
        elif start_date is not None and end_date is None:
            params['date__gte'] = start_date
            params['date__lte'] = today
        elif start_date is None and end_date is not None:
            params['date__gte'] = today
            params['date__lte'] = end_date
        queryset = Product.objects.filter(**params)
        is_filtered = True
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

