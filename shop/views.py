from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from shop.models import Product


class GetProductList(APIView):
    def get(self, request, *args, **kwargs):
        queryset = Product.objects.filter(is_archive=False).order_by('-date')
        page = request.GET.get('page', 1)
        paginator = Paginator(queryset, 10)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        return render(request, "index.html", context={"products": products})


class ArchiveProduct(APIView):
    def post(self, request, id):
        product = Product.objects.get(id=id)
        product.is_archive = True
        product.save()
        return redirect('get_product_by_status_url')


class ArchivedProducts(APIView):
    def get(self, request, *args, **kwargs):
        products = Product.objects.filter(is_archive=True)
        page = request.GET.get('page', 1)
        paginator = Paginator(products, 10)
        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            products = paginator.page(1)
        except EmptyPage:
            products = paginator.page(paginator.num_pages)
        return render(request, 'archive.html', context={"products": products})


class RemoveFromArchive(APIView):
    def post(self, request, id):
        product = Product.objects.get(id=id)
        product.is_archive = False
        product.save()
        return redirect('archive_list_url')
