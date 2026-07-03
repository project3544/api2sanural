from django.contrib import admin
from cash_flow.models import Provider, Product

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    """Настройка панели управления поставщиками"""
    list_display = ('name', 'is_active', 'first_api_key', 'second_api_key')
    list_filter = ('is_active',)
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Настройка панели управления товарами Санурала"""
    list_display = ('sku', 'title', 'category', 'purchase_price', 'retail_price', 'stock', 'provider')
    list_filter = ('provider', 'category', 'stock')
    search_fields = ('sku', 'title', 'category')
    readonly_fields = ('updated_at',)
    list_editable = ('retail_price', 'stock')  # Санурал меняет цены прямо из таблицы!
    list_per_page = 50