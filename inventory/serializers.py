from rest_framework import serializers, status
from rest_framework.serializers import ValidationError
from rest_framework.validators import UniqueValidator
from rest_framework.response import Response
from inventory.models import (
    Brand, Category, Product, ProductInventory, Stock)

#for nested serilaizer we should use in one to show the different serialize value of many



class ProductInventorySerializer(serializers.ModelSerializer):
    #TODO to show that product is out of inventory
    # stock_list = StockSerializer(many=True, read_only=True)
    class Meta:
        model = ProductInventory
        fields = [
            "id",
            "sku",
            "upc",
            "store_price",
            "is_on_sale", 
            "sale_price",
            "product",
            "brand",  
            # "stock_list",
        ]
        read_only = True
    


class ProductSerializer(serializers.ModelSerializer):
    product_inventory = ProductInventorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = [
            "id",
            "slug",
            "name",
            "quantity",
            "description",
            "price",
            "image",
            "thumbnail",
            "category",
            "is_active",
            "get_image",
            "product_inventory",   
        ]
        read_only=True
        

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    
    class Meta:
        model = Category
        fields = [
            "id", 
            "name", 
            "slug",
            "products",
            # "product_inventory",
           
        ]

class BrandSerializer(serializers.ModelSerializer):
    inventory = ProductInventorySerializer(many=True, read_only=True)
    
    class Meta:
        model= Brand
        fields=[
            "id",
            "name",
            "inventory"
        ]

class StockSerializer(serializers.ModelSerializer):
    # inventorylists = ProductInventorySerializer(many=True, read_only=True)
    class Meta:
        model = Stock
        fields = [
            "id",
            "units", 
            "units_sold",
            "product_inventory",  
            # "inventorylists", 
        ]
     
        
action_serializer_dict_product_inventory = {
    "create": ProductInventorySerializer,
    "list":ProductInventorySerializer,
    "retrieve":ProductInventorySerializer,
    "destroy":ProductInventorySerializer,
    "update":ProductInventorySerializer,
    "partial_update":ProductInventorySerializer,
}
   
   
action_serializer_dict_product = {    
    "create": ProductSerializer,
    "list":ProductSerializer,
    "retrieve":ProductSerializer,
    # "destroy":ProductSerializer,
    "update":ProductSerializer,
    "partial_update":ProductSerializer,
}  
action_serializer_dict_category = {
    "create": CategorySerializer,
    "list":CategorySerializer,
    "retrieve":CategorySerializer,
    "destroy":CategorySerializer,
    "update":CategorySerializer,
    "partial_update":CategorySerializer,
}
          
action_serializer_dict_brand ={
    "create":BrandSerializer,
    "list": BrandSerializer,
    "retrieve":BrandSerializer,
    "destroy":BrandSerializer,
    "update":BrandSerializer,
    "partial_update":BrandSerializer,   
}   

action_serializer_dict_stock = {
    "create":StockSerializer,
    "list": StockSerializer,
    "retrieve":StockSerializer,
    "destroy":StockSerializer,
    "update":StockSerializer,
    "partial_update":StockSerializer,   
}