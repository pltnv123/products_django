from django.core.cache import cache
from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.contrib.auth.models import User


# Товар для нашей витрины
class Product(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,  # названия товаров не должны повторяться
    )
    description = models.TextField()
    quantity = models.IntegerField(validators=[MinValueValidator(0, 'Quantity should be >= 0')])
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='products',  # все продукты в категории будут доступны через поле products
    )
    price = models.FloatField(validators=[MinValueValidator(0.0, 'Price should be >= 0.0')])

    # допишем свойство, которое будет отображать есть ли товар на складе
    @property
    def on_stock(self):
        return self.quantity > 0

    def __str__(self):
        return f'{self.name} {self.quantity}'

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])          # == f'/products/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'product-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его


# Категория, к которой будет привязываться товар
class Category(models.Model):
    # названия категорий тоже не должны повторяться
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f'{self.name}'


class Material(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# class ProductMaterial(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     material = models.ForeignKey(Material, on_delete=models.CASCADE)


# Product.objects.filter(productmaterial__material)  (для фильтров можно добавлять)


class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
