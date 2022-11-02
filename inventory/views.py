from datetime import datetime
from http.client import CannotSendHeader
# from crypt import methods
from django.http import Http404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from inventory.serializers import (
    ProductInventorySerializer, ProductSerializer,
    CategorySerializer, StockSerializer,BrandSerializer,
    
    action_serializer_dict_product, action_serializer_dict_category,
    action_serializer_dict_product_inventory, action_serializer_dict_brand,
    action_serializer_dict_stock)

from inventory.models import (
    ProductInventory, Product, Category, Stock, Brand)

from inventory.constants import (
    _UPDATED_SUCCESSFULLY, _ACTIVATED, _PRODUCT_CREATED,
    _PRODUCT_DELETED, _PARTIALLY_UPDATED,_CATEGORY_CREATED,
    _CATEGORY_DELETED, _PARTIALLY_UPDATED_CATEGORY,
    _UPDATED_BRAND, _BRAND_CREATED, _STOCK_CREATED,
    _STOCK_DELETED,_STOCK_UPDATED)


class ProductInventoryViewSet(viewsets.ModelViewSet):
    serializer_class = ProductInventorySerializer
    queryset = ProductInventory.objects.all()
    
    def get_serializer_class(self):
        return action_serializer_dict_product_inventory.get(self.action, super(ProductInventoryViewSet, self).get_serializer_class())

    
    def get_queryset(self):
        return ProductInventory.objects.all()
    
    def perform_create(self, serializer):
        serializer.save()
        # serializer.save(owner=self.request.user) if reltion with user as owner
    def create(self, request, *args, **kwargs):
        product_inventory_data = request.data
        new_product_inventory_data = ProductInventory.objects.create(
            product=Product.objects.get(id=product_inventory_data["product"]),
            brand = Brand.objects.get(id=product_inventory_data["brand"]),
            # stock = Stock.objects.get(id= product_inventory_data["stock"]),
            sku= product_inventory_data["sku"],
            upc = product_inventory_data["upc"],
            store_price = product_inventory_data["store_price"],
            sale_price = product_inventory_data["sale_price"],
            # is_on_sale =  product_inventory_data[(True, False,  None),],  
        )
        # new_product_inventory_data.is_on_sale = True
        if new_product_inventory_data.store_price < new_product_inventory_data.sale_price:
            new_product_inventory_data.is_on_sale = True
        else:
            False    
        new_product_inventory_data.save()
        serializer = self.get_serializer(new_product_inventory_data)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = ProductInventorySerializer(instance=instance)
        return Response(serializer.data)
   
    
        
    def list(self, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer =ProductInventorySerializer(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        print("here", queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)    
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            
            if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
                instance._prefetched_objects_cache = {}
            return Response( {"message": _UPDATED_SUCCESSFULLY, "data":serializer.data},
                            status=status.HTTP_201_CREATED)
        except Http404:
            pass
        
    @action(detail=False, methods=["post"], url_path="activate")
    def activate(self, request, *args, **kwargs):
        product_inventory = ProductInventory.objects.all()
        # serializer=self.get_serializer(data=kwargs)
        # serializer.is_valid(raise_exception=True)
        for inventory in product_inventory:
            inventory.is_active= "is_active"
            inventory.is_active = True
            inventory.save()
        # product_inventory.is_active=True
            inventory.activated_at = datetime.utcnow()
        # product_inventory.save()
        return Response({"messgae": _ACTIVATED},
                        status=status.HTTP_200_OK)
        
    
    
    
    
class ProductViewSet(viewsets.ModelViewSet):
    queryset= Product.objects.all()
    serializer_class = ProductSerializer 
    
    def get_serializer_class(self):
        return action_serializer_dict_product.get(self.action, 
                                        super(ProductViewSet, self).get_serializer_class())
    
    def get_queryset(self):
        queryset = Product.objects.all()
        return queryset
    
    def create(self, request, *args, **kwargs):
        product_data = request.data
        new_product_data = Product.objects.create(
            category = Category.objects.get(id=product_data["category"]),
            name = product_data["name"],
            slug= product_data["slug"],
            description = product_data["description"],
            price = product_data["price"],
            image = product_data["image"],
            thumbnail = product_data["thumbnail"],
            quantity = product_data["quantity"]
            
        )
        new_product_data.save()
        serializer = self.get_serializer(new_product_data)
        return Response({"message": _PRODUCT_CREATED, "data":serializer.data}, 
                        status=status.HTTP_201_CREATED)
        
    def list(self, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = ProductSerializer(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        print("here", queryset)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, *args, **kwargs):
        instance = self.get_object()
        serializer = ProductSerializer(instance=instance)
        return Response(serializer.data)
    
    
        
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"message": _PARTIALLY_UPDATED}, status=status.HTTP_201_CREATED)



class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_queryset(self):
        return Category.objects.all()
    
    def get_serializer_class(self):
        return action_serializer_dict_category.get(self.action,
                                          super(CategoryViewSet, self).get_serializer_class())
        
    def create(self, request, *args, **kwargs):
        category_data = request.data
        new_category = Category.objects.create(
            name = category_data["name"],
            slug = category_data["slug"],
        )
        new_category.save()
        serializer=CategorySerializer(new_category)
        return Response(
            {
                "message":_CATEGORY_CREATED , 
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED
        )
    
    def list(self, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = CategorySerializer(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True) 
        
        return Response(serializer.data)
    
    def retrieve(self, *args, **kwargs):
        instance= self.get_object()
        serializer = CategorySerializer(instance=instance)
        return Response(serializer.data)
    
    def destroy(self, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                "message":_CATEGORY_DELETED,
            },
            status=status.HTTP_204_NO_CONTENT
        )
        
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {
                "message":_PARTIALLY_UPDATED_CATEGORY,
                "data": serializer.data,
            },
            status = status.HTTP_201_CREATED
        )
            
            
class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    
    def get_serializer_class(self):
        return action_serializer_dict_brand.get(
            self.action, super(BrandViewSet, self).get_serializer_class()
        )            
    
    def get_queryset(self):
        return Brand.objects.all()
    
    def create(self, request, *args, **kwargs):
        brand_data = request.data
        new_brand = Brand.objects.create(
            name = brand_data["name"],
        )
        new_brand.save()
        serializer = BrandSerializer(new_brand)
        return Response(
            {
                "message": _BRAND_CREATED,
                "data": serializer.data
            },
            status = status.HTTP_201_CREATED
        )
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = BrandSerializer(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many = True)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = BrandSerializer(instance=instance)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)
               
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response( {"message": _UPDATED_BRAND, "data":serializer.data},
                            status=status.HTTP_201_CREATED)
       
        
class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
       
       
    def get_serializer_class(self):
        s = action_serializer_dict_stock.get(self.action, super(StockViewSet, self).get_serializer_class())
        return s

    def get_queryset(self):
        return Stock.objects.all()
    
    def create(self, request, *args, **kwargs):
        stock_data = request.data
        # stock_data["product_inventory"] = request.product_inventory.id
        new_stock_data = Stock.objects.create(
            units = stock_data["units"],
            units_sold = stock_data["units_sold"],
        
        )
        new_stock_data.save()
        
        # inventory_data = ProductInventory.objects.create(
        #     sku = stock_data["sku"],
        #     upc = stock_data["upc"],
        #     retail_price = stock_data["retail_price"],
        #     store_price = stock_data["store_price"],
        #     sale_price = stock_data["saleprice"],
            
        # )
        # inventory_data.save() 
        serializer = self.get_serializer(data=stock_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        return Response(
            {
                "message": _STOCK_CREATED,
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED
        )      
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = StockSerializer(queryset, many=True)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)  

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = StockSerializer(instance=instance)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                "message": _STOCK_DELETED,
                
            },
            status=status.HTTP_204_NO_CONTENT
        )
    
    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {
                "message": _STOCK_UPDATED,
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED
        )    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    