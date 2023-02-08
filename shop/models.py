from django.db import models


class Warehouse(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=500)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.DO_NOTHING, related_name='product', null=True)
    posting_number = models.CharField(max_length=250, blank=True, null=True)
    quantity = models.IntegerField()
    date = models.DateTimeField()
    artikul = models.CharField(max_length=300)
    is_archive = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ArticleNumber(models.Model):
    name = models.CharField(max_length=255)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.DO_NOTHING, related_name='article_number', null=True)

    def __str__(self):
        return self.name
