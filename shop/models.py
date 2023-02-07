from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=500)
    posting_number = models.CharField(max_length=250, blank=True, null=True)
    quantity = models.IntegerField()
    date = models.DateTimeField()
    artikul = models.CharField(max_length=300)
    is_archive = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
