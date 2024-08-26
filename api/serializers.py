from rest_framework import serializers
from .models import Product, Material, Warehouse, ProductMaterials


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'material', 'remainder', 'price']


class ProductMaterialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMaterials
        fields = ['product', 'material', 'quantity']


class ProductSerializer(serializers.ModelSerializer):
    product_materials = ProductMaterialsSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['name', 'code', 'product_materials']
