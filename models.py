from django.db import models

class Provider(models.Model):
    """Модель поставщиков сантехники Санурала"""
    name = models.CharField(max_length=255, verbose_name="Название поставщика")
    first_api_key = models.CharField(max_length=255, verbose_name="Первый API Ключ")
    second_api_key = models.CharField(max_length=255, verbose_name="Второй API Ключ", blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name="Статус интеграции")

    def __str__(self):
        return self.name

class Product(models.Model):
    """Модель товаров интернет-магазина Sanural"""
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, related_name="products", verbose_name="Поставщик")
    sku = models.CharField(max_length=100, unique=True, verbose_name="Артикул")
    title = models.CharField(max_length=255, verbose_name="Наименование")
    category = models.CharField(max_length=255, verbose_name="Категория")
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Закупочная цена")
    retail_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Розничная цена")
    stock = models.IntegerField(default=0, verbose_name="Остаток на складе")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Последнее обновление")

    def __str__(self):
        return f"{self.sku} - {self.title}"