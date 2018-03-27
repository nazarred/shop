from django.contrib import admin
from .models import Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'add_date', 'get_total_price']
    list_filter = ['add_date']

    def get_form(self, request, obj=None, **kwargs):
        form = super(OrderAdmin, self).get_form(request, obj, **kwargs)
        if obj:
            form.base_fields['products'].queryset = obj.products.all()
        return form


admin.site.register(Order, OrderAdmin)