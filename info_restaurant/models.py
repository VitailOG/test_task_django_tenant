from typing import Type

from django.db import models

from main.models import Restaurant


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    type = models.CharField(verbose_name='Тип меню', max_length=50)

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'


class Category(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(verbose_name='Назва категорії', max_length=50)

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return f'Menu type id -> {self.menu.id} - {self.name}'


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(verbose_name='Назва продукту', max_length=256)
    price = models.DecimalField(verbose_name='Ціна продукту', max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукти'
