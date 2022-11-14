from django.contrib import admin
from product.models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):  # pragma nocover
    def has_add_permission(self, request) -> bool:
        return False
    
    def has_change_permission(self, request, obj=...) -> bool:
        return False
    
    def has_delete_permission(self, request, obj=...) -> bool:
        return True