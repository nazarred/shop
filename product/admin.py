from django.contrib import admin
from .models import *


admin.site.register(ProductComment)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0


admin.site.register(ProductImage)


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

    class Meta:
        model = Product


admin.site.register(Product, ProductAdmin)
