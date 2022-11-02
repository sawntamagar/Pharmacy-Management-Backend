from django.urls import path
from rest_framework import routers

# from order.views import(
#     OrderViewSet
# )

from order.views import (
    OrderCreateApi,
    OrderItemCreateApi, 
    OrderListApi, OrderItemUpdateApi,
    OrderRetrieve,OrderItemRetrieveApi,
    OrderUpdate,OrderItemListApi,
    OrderDestroyApi, OrderItemDestroyApi,
    # OrderItemAdd,
    )

router = routers.DefaultRouter()
# router.register(r"order", OrderCreateApi, basename="order")
# router.register(r"order_item", OrderItemViewSet, basename="order_item")

urlpatterns = [
   path("order/", OrderCreateApi.as_view(), name="order_create_api"),
   path("orderlist/", OrderListApi.as_view(), name="order-list"),
   path("orderitem/", OrderItemCreateApi.as_view(), name="order-itme"),
   path("order/<int:id>/", OrderRetrieve.as_view(), name="order"),
   path("order/<int:id>/update/", OrderUpdate.as_view(), name = "update_order"),
   path("order/<int:id>/destroy/", OrderDestroyApi.as_view(), name="delete_order"),
   
   
   path("orderitem/<int:id>/retrieve/", OrderItemRetrieveApi.as_view(), name="retrieve_order_item"),
   path("orderitem/<int:id>/destroy/", OrderItemDestroyApi.as_view(), name="desroy_order_item"),
   path("orderitem/<int:id>/update/", OrderItemUpdateApi.as_view(), name="update_order_item"),
   path("orderitem/list/", OrderItemListApi.as_view(), name="list_oreder_item"),
   
#    path("/order_item/add/<int:id>/", OrderItemAdd.as_view(), name = "order_item_add_view" )
    
  
   
   
   
    ]


urlpatterns = urlpatterns +  router.urls
