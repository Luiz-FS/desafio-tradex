from django.contrib import admin
from product_cost.models import ProductCost

@admin.register(ProductCost)
class ProductCostAdmin(admin.ModelAdmin):  # pragma nocover
    def has_add_permission(self, request) -> bool:
        return False
    
    def has_change_permission(self, request, obj=...) -> bool:
        return False
    
    def has_delete_permission(self, request, obj=...) -> bool:
        return False