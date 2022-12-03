from typing import Type

from django.db import models

from main.models import Restaurant


class NullForeignKey(models.ForeignKey):

    def __init__(
        self,
        to: Type[models.Model],
        on_delete: callable = models.SET_NULL,
        related_name: str = None,
        related_query_name: str = None,
        limit_choices_to=None,
        parent_link: bool = False,
        to_field=None,
        db_constraint: bool = True,
        **kwargs
    ):
        """ Кастомний клас який за замовчування є необов'язковим
        """
        super().__init__(
            to, on_delete, related_name, related_query_name, limit_choices_to,
            parent_link, to_field, db_constraint, **kwargs
        )
        self.null = True


class Menu(models.Model):
    restaurant = NullForeignKey(Restaurant)
    type = models.CharField(verbose_name='Тип меню', max_length=50)

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'


class Category(models.Model):
    menu = NullForeignKey(Menu, related_name='categories')
    name = models.CharField(verbose_name='Назва категорії', max_length=50)

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return f'Menu type id -> {self.menu.id} - {self.name}'


class Product(models.Model):
    category = NullForeignKey(Category, related_name='products')
    name = models.CharField(verbose_name='Назва продукту', max_length=256)
    price = models.DecimalField(verbose_name='Ціна продукту', max_digits=5, decimal_places=2)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукти'
