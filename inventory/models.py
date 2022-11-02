from io import BytesIO
from PIL import Image

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.files import File



 #one product has many product inventory In one to many relationship the one should be
 #written in top and many shoul be written in down
  
class Category(models.Model):
    name = models.CharField(max_length=255, null=True)
    slug = models.SlugField()
    
    class Meta:
        ordering = ('name',)
        verbose_name_plural = _("categories")
        
    def __str__(self):
       return self.name
  
    def get_absolute_url(self):
        return f'/{self.slug}'
    
    
class Product(models.Model):
    name = models.CharField(max_length=255,)
    slug = models.SlugField(max_length=255,)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, null=True)
    description = models.TextField(blank=True)
    quantity = models.IntegerField(default=1, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-date_added',)

    def __str__(self): 
        return self.name

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'
    
    def get_image(self):
        if self.image:
            return 'http://127.0.0.1.8000' + self.image.url
        return ''
    
    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1.8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return 'http://127.0.0.1.8000' + self.thumbnail.url
            else:
                return ''
            
    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        
        thumb_io = BytesIO()
        img.save(thumb_io, 'jpeg', quality=85)
        
        thumbnail = File(thumb_io, name= image.name)
        
        return thumbnail
    
class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True, null=True)
    
    def __str__(self):
        return self.name 
    
    
  

class ProductInventory(models.Model):
    sku = models.CharField(max_length=20,  null = True)
    upc = models.CharField(max_length=12, null = True)
    product = models.ForeignKey(Product, related_name="product", on_delete=models.PROTECT,
         null=True)
    brand = models.ForeignKey( Brand, related_name="brand", on_delete=models.SET_NULL,
                                blank=True,null=True)
    is_active = models.BooleanField(default=False, null=True, blank=True)
    retail_price =models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True,
                                      error_messages={
                                          "name":{
                                              "max_length": _("the price must be between 0 and 999.99"),
                                        },
                                    },
                                )
    store_price = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True,
                                      error_messages={
                                          "name":{
                                              "max_length": _("the price must be between 0 and 999.99"),
                                        },
                                    },
                                )
    sale_price = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True,
                                     error_messages={
                                        "name": {
                                            "max_length": _("the price must be between 0 and 999.99"),
                                        },
                                    },
                                )
    # quantity = models.IntegerField(null=True, blank=True)
    is_on_sale = models.BooleanField(default=False,null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    activated_at = models.DateTimeField(auto_now=True)
    
    # def __str__(self):
    #     return self.sku
    
    
class Stock(models.Model):
    product_inventory = models.OneToOneField(ProductInventory, related_name="product_inventory",
                                             on_delete=models.PROTECT, null=True)
    last_checked = models.DateTimeField(null=True, blank=True)
    units = models.IntegerField(default=0)
    units_sold = models.IntegerField(default=0)
    
            
    
    
        