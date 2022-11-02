from django.db import models
from django.db.models import F

from account.models import PmsUser
from inventory.models import Product

               

class Order(models.Model):
    ORDER_STATUS_PENDING = "P"
    ORDER_STATUS_COMPLETED = "C"
    ORDER_STATUS_FAILED = "F"
    
    ORDER_STATUS_CHOICES = [
        (ORDER_STATUS_PENDING, "Pending"),
        (ORDER_STATUS_COMPLETED, "Complete"),
        (ORDER_STATUS_FAILED, "Fail"),
    ]

    user = models.ForeignKey(PmsUser, related_name='orders', on_delete=models.CASCADE)
    # user_email = models.EmailField(max_length=100)
    # first_name = models.CharField(max_length=100)
    # last_name = models.CharField(max_length=100)
    ordered_date = models.DateTimeField(auto_now_add = True, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    address = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=100)
    place =models.CharField(max_length=100)
    is_paid = models.BooleanField(default=False)
    # stripe_token =models.CharField(max_length=100)
    comment = models.TextField(max_length=100, blank=True)
    #payment
    order_status = models.CharField(max_length=1, choices=ORDER_STATUS_CHOICES,
                                      default=ORDER_STATUS_PENDING)
    
    # def __str__(self):
    #     return self.user_email + '-' + self.ordered_date.strftime("%b. %-d, %Y, %-I:%M %p")
    
    # def get_total_price(self):
    #     return self.product.get_total_price()
    
    @property
    def total_price(self):
        return sum([_.price for _ in self.items_set.all()]) #related name is items

    def __str__(self):
        return self.user.email
    
    class Meta:
        verbose_name_plural = "Orders"
        ordering = ('-id',)
    
      
    @staticmethod
    def create_order(user,  place,comment,zipcode, address, is_paid=False, ordered=False):
        order = Order()
        order.user = user
        order.ordered = ordered
        order.address = address
        order.is_paid = is_paid
        order.place = place
        order.comment = comment
        order.zipcode = zipcode
        order.save()
        return order
    
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, related_name='product_order', on_delete=models.CASCADE)
   
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=8, decimal_places=2, null=True)
        
    def __str__(self):
         return  '%s' % self.id
               
    def calculate_total_price(self):
        total = float(self.product.price) * int(self.quantity)
        print("The total Price is",total)
        
        return total
    
    def save(self, *args, **kwargs):
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)
               
    # def calculate_quantity_in_product_after_selling(self):
    #     remaining_quantity = float(self.product.quantity) - float(self.quantity)
    #     return remaining_quantity
    
    # def save(self, *args, **kwargs):
    #     self.product.quantity = self.calculate_quantity_in_product_after_selling()
    #     super().save(*args, **kwargs)
        
    # def calculate_added_quantity_in_order_item(self):
    #     added_quantity = float(self.quantity) + float(self.product.quantity)
    #     return added_quantity
    
    # def save(self, *args, **kwargs):
    #     self.quantity = self.calculate_added_quantity_in_order_item()
    #     super().save(*args, **kwargs)
        
        
        
    
    @staticmethod
    def create_order_item(order, product, quantity, total_price):
        order_item = OrderItem()
        order_item.order = order
        order_item.product = product
        order_item.quantity = quantity
        order_item.total_price = total_price
        order_item.save()
        return order_item
        
    
     
     
        
        