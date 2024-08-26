from django.contrib import admin

from .models import Product, Material, ProductMaterials, Warehouse


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(ProductMaterials)
class ProductMaterialAdmin(admin.ModelAdmin):
    list_display = ('product', 'material', 'quantity')


@admin.register(Warehouse)
class WarehousesAdmin(admin.ModelAdmin):
    list_display = ('material', 'remainder', 'price')
