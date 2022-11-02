from rest_framework import serializers

from order.models import Order, OrderItem
from account.serializers import PmsUserDetailSerializer



class OrderItemSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(read_only=True)
    total_price = serializers.FloatField(read_only=True)
    # total_price = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields = [
            "id",
            "order",
            "quantity",
            "total_price",
            "product",    
        ]
        read_only=True
        
    # def get_total_price(self, obj):
    #     return obj.total_price    



class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    total_price = serializers.ReadOnlyField()
    
    class Meta:
        model = Order
        fields =[
            "id",
            "user",
            "order_items",
            "total_price",
            "ordered_date",
            "ordered",
            "address",
            "zipcode",
            "place",
            "is_paid",
            "comment",
            "order_status",
            
        ]

    def create(self, validated_data):
        user = self.context['request'].user
        if not user.is_active:
            order_items = validated_data.pop('order_items')
            order = Order.objects.create(user=user, **validated_data)
            for order_item in order_items:
                OrderItem.objects.create(order=order, **order_item)
                
            return order
        else:
            raise serializers.ValidationError("You are not Customer. Please Register first....")
        


class OrderListSerializer(serializers.ModelSerializer):
    orderitems = OrderSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    # total_price = serializers.ReadOnlyField()
    
    class Meta:
        model = Order
        fields =[
            "id",
            "user",
            "orderitems",
            # "total_price",
            "ordered_date",
            "ordered",
            "address",
            "zipcode",
            "place",
            "is_paid",
            "comment",
            "order_status",
            
        ]



class OrderUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model= Order
        fields = [
            "address",
            "place",
            "zipcode",
            "comment",
        ]

class OrderItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields =["quantity"]

action_serializer_dict_order_list={
    "list":OrderListSerializer,
}
        
action_serializer_dict_order = {
    "list": OrderSerializer,
    "create": OrderSerializer,
    
}            

action_serializer_dict_order_item = {
    "list":OrderItemSerializer,
    "create": OrderItemSerializer,
}












# class OrderCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Order
#         fields =[
#             "id",
#             # "user",
#             "user_email",
#             "first_name",
#             "last_name",
#             "ordered",
#             "address",
#             "zipcode",
#             "place",
#             "is_paid",
#             "comment",
#             "order_status",
            
#             ]
        
# class OrderDetailSerializer(serializers.ModelSerializer):
#     user = PmsUserDetailSerializer()
#     class Meta:
#         model = Order
#         fields = [
#             "id",
#             "user",
#             "user_email",
#             "first_name",
#             "last_name",
#             "ordered",
#             "address",
#             "zipcode",
#             "place",
#             "is_paid",
#             "comment",
#             "order_status",
            
#         ]        
        
# class OrderItemCreateSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = OrderItem
#         fields = [
#             "id",
#             "order",
#             "product",
#             "quantity",
#             "total_price",
           
#         ]
            
            
# class OrderItemDetailSerializer(serializers.ModelSerializer):
#     order_list = OrderDetailSerializer(many=True, read_only=False)
    
#     class Meta:
#         model = OrderItem
#         fields =[
#             "id",
#             "quantity",
#             "total_price",
#         ]            
        
        
        
# action_serializer_dict_order = {
#     "list":OrderDetailSerializer,
#     "create":OrderCreateSerializer,
#     "retrieve":OrderDetailSerializer,
#     "update": OrderCreateSerializer,
#     "partial_update": OrderCreateSerializer,
# }        

# action_serialzer_dict_order_item = {
#     "list":OrderItemDetailSerializer,
#     "create":OrderItemCreateSerializer,
#     "retrieve": OrderItemDetailSerializer,
#     "update": OrderItemCreateSerializer,
#     "partial_update": OrderItemCreateSerializer,
# }