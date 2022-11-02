
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r"", include("account.urls")),
    path(r"", include("inventory.urls")),
    path(r"", include("order.urls")),
   
]
