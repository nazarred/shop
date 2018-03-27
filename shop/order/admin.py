from django.contrib import admin
from .models import Order, ProductInOrder


admin.site.register(ProductInOrder)


class ProductInOrderInline(admin.TabularInline):
    model = ProductInOrder
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    inlines = [ProductInOrderInline]
    list_display = ['__str__', 'add_date', 'total_order_price']
    list_filter = ['add_date']

    # def get_form(self, request, obj=None, **kwargs):
    #     form = super(OrderAdmin, self).get_form(request, obj, **kwargs)
    #     if obj:
    #         form.base_fields['products'].queryset = obj.products.all()
    #     return form


admin.site.register(Order, OrderAdmin)
