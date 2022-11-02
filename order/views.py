from tracemalloc import get_object_traceback
from xml.dom import ValidationErr
from django.shortcuts import get_object_or_404
from django.http import Http404


from rest_framework import viewsets, generics,status, exceptions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from account.models import PmsUser
from inventory.models import Product
from order.models import Order, OrderItem
from order.seriaizers import (
    OrderListSerializer,
    OrderSerializer,
  
    OrderItemSerializer,
    OrderUpdateSerializer,
    OrderItemUpdateSerializer,
   
    action_serializer_dict_order,
    action_serializer_dict_order_item,
    action_serializer_dict_order_list,
    )

from order.constants import (
     _ORDER_CREATED,  _ORDER_LIST,
     _ORDER_ITEM_CREATED,
     _UPDATE_ORDER,_ORDER_ITEM_DELETED,
    _ORDER_DELETED, _ORDER_ITEM_LIST, _ORDER_ITEM_RETRIEVE,
    _UPDATE_ORDER_ITEM
)


# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderCreateSerializer


# class OrderItemViewSet(viewsets.ModelViewSet):
#     queryset = OrderItem.objects.all()
#     serializer_class = OrderItemCreateSerializer


class OrderCreateApi(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    
    def get_queryset(self):
        order = Order.objects.all()
        return order
    
    def get_serializer_class(self):
        action_serializer = action_serializer_dict_order.get(
            self.action, super(OrderCreateApi, self).get_serializer_class()
        )
        return action_serializer
        
    def create(self, request, *args, **kwargs):
        order_by_user = request.data
        new_order_by_user = Order.objects.create(
            user = PmsUser.objects.get(id=request.user.id),
            # user_email= order_by_user["user_email"],
            # first_name = order_by_user["first_name"],
            # last_name = order_by_user["last_name"],
            address = order_by_user["address"],
            place = order_by_user["place"],
            comment = order_by_user["comment"],
            order_status = order_by_user["order_status"],
            # is_paid = order_by_user["is_paid", False],
            zipcode = order_by_user["zipcode"],
        )
        new_order_by_user.save()
        serializer = OrderSerializer(new_order_by_user)
        return Response(
            {"message":_ORDER_CREATED,
             "data": serializer.data},
            status = status.HTTP_201_CREATED
        )
        
class OrderListApi(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    
    def get_queryset(self):
        return Order.objects.all()
    
    def get_serializer_class(self):
        serializer = action_serializer_dict_order_list.get(
            self.action, super(OrderListApi, self).get_serializer_class()
        )
        return serializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = OrderListSerializer(queryset, many=True)
        return Response(
            {"message": _ORDER_LIST,
            "data": serializer.data
            },
            status=status.HTTP_200_OK
        )        
    
class OrderRetrieve(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class =  OrderSerializer
    
    def retrieve(self,request, id=None):
        queryset = Order.objects.all()
        order = get_object_or_404(queryset, id=id)
        serializer = OrderSerializer(order)
        return Response(serializer.data)
        
        
class OrderUpdate(generics.UpdateAPIView):
    queryset=Order.objects.all()
    serializer_class = OrderUpdateSerializer
    
    def update(self, request, id, *args, **kwargs):
        queryset=Order.objects.all()
        order_to_be_update = get_object_or_404(queryset, id=id)
        serializer= OrderUpdateSerializer(order_to_be_update,data=request.data )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    "message":_UPDATE_ORDER,
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )    
        raise ValidationErr(serializer.errors)
    
    
class OrderDestroyApi(generics.DestroyAPIView):
    queryset=Order.objects.all()
    serializer_class = OrderSerializer
    
    def get_object(self, id):
        try:
            return Order.objects.get(id=id)
        except Order.DoesNotExist:
            raise Http404
    
    def destroy(self, request, id,*args, **kwargs):
        order = self.get_object(id=id)
        order.delete()
        return Response(
            {
                "message": _ORDER_DELETED,
                
            },
            status=status.HTTP_204_NO_CONTENT
        )
        
class OrderItemCreateApi(generics.CreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    
    def get_queryset(self):
        return OrderItem.objects.all()
    
    def get_serializer_class(self):
        return action_serializer_dict_order_item.get(
            self.action, super(OrderItemCreateApi, self).get_serializer_class()
        )

    def create(self, request, *args, **kwargs):
        order_item = request.data
        # product = Product.objects.get_object()
        
        
        new_order_item = OrderItem.objects.create(
            order = Order.objects.get(id = order_item["order"]),
            product = Product.objects.get(id=order_item["product"]),
            quantity = order_item["quantity"],
            # total_price = order_item["total_price"]
        )    
        # if product.quantity<= self.quantity:
        #     return Response(
        #         {
        #             "message":"you have ordered more than the quantity of product"
        #         },
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
            
    
        new_order_item.save()
        serializer = OrderItemSerializer(new_order_item)
        return Response(serializer.data)
    

# class OrderItemAdd(generics.ListAPIView):
#     queryset=OrderItem.objects.all()
#     serializer_class = OrderItemSerializer
    
#     def list(self,request,id,*args,**kwargs):
#         # user = request.user
#         order_item_id = OrderItem.objects.get(id=id)
#         ordered_product = order_item_id.get(id=id)
#         product = Product.objects.filter(quantity='quantity')
#         if product.quantity <= 0 :
#             return Response(
#                  data={
#                     "detail": "this item is sold out try another one !",
#                     "code": "sold_out"}
#             )  
            
#         ordered_product.quantity = ordered_product.quantity +  float(self.product.quantity)        
#         product_quantity = product.quantity - float(self.ordered_product.quantity) 
        
        
        
#         order=request.order
#         order_item = OrderItem.objects.filter(order=order)
#         added_order_item = order_item.get(id=id)
#         product = get_object_or_404(Product, id = added_order_item.product.id)
#         if product.quantity <=0 :
#             return Response(
#                     data={
#                     "detail": "this item is sold out try another one !",
#                     "code": "sold_out"
#                     }
#             )

#         added_order_item.quantity = added_order_item.quantity + float(OrderItem.quantity)
#         product.quantity = product.quantity - float(Product.quantity)
#         product.save()
#         added_order_item.save()
#         return Response (
#             {
#                 "message": "product is added successfully",
#             },
#             status=status.HTTP_200_OK
#         )





    
class OrderItemListApi(generics.ListAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    
    def get_queryset(self):
        return OrderItem.objects.all()
    
    def get_serializer_class(self):
        serializer = action_serializer_dict_order_item.get(
            self.action, super(OrderItemListApi, self).get_serializer_class()
        )
        return serializer
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = OrderItemSerializer(queryset, many=True)
        return Response(
            {"message": _ORDER_ITEM_LIST,
            "data": serializer.data
            },
            status=status.HTTP_200_OK
        )        
    
class OrderItemRetrieveApi(generics.RetrieveAPIView):
    queryset = OrderItem.objects.all()
    serializer_class =  OrderSerializer
    
    def retrieve(self,request, id=None):
        queryset = OrderItem.objects.all()
        order = get_object_or_404(queryset, id=id)
        serializer = OrderItemSerializer(order)
        return Response(
            {
                "message":_ORDER_ITEM_RETRIEVE,
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )
        
        
class OrderItemUpdateApi(generics.UpdateAPIView):
    queryset=OrderItem.objects.all()
    serializer_class = OrderItemUpdateSerializer
    
    def update(self, request, id, *args, **kwargs):
        queryset=OrderItem.objects.all()
        order_to_be_update = get_object_or_404(queryset, id=id)
        serializer= OrderItemUpdateSerializer(order_to_be_update,data=request.data )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(
                {
                    "message":_UPDATE_ORDER_ITEM,
                    "data": serializer.data
                },
                status=status.HTTP_201_CREATED
            )    
        raise ValidationErr(serializer.errors)
    
 
    
class OrderItemDestroyApi(generics.DestroyAPIView):
    queryset=OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    
    def get_object(self, id):
        try:
            return Order.objects.get(id=id)
        except OrderItem.DoesNotExist:
            raise Http404
    
    def destroy(self, request, id,*args, **kwargs):
        order_item = self.get_object(id=id)
        order_item.delete()
        return Response(
            {
                "message": _ORDER_ITEM_DELETED,
                
            },
            status=status.HTTP_204_NO_CONTENT
        )
        
    
    