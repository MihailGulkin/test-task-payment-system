from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=100, decimal_places=2)

    def __str__(self):
        return f'{self.pk} - {self.name} '


class Order(models.Model):
    items = models.ManyToManyField(Item)

    def __str__(self):
        return f'{self.pk}'
