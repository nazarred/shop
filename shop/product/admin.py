from django.contrib import admin
from .models import Product, ProductRating, ProductComment, ProductImage


class ProductRatingInline(admin.TabularInline):
    model = ProductRating
    extra = 0


class ProductCommentInline(admin.TabularInline):
    model = ProductComment
    extra = 0


class ProductCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'product']

    class Meta:
        model = ProductComment


admin.site.register(ProductComment, ProductCommentAdmin)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0


admin.site.register(ProductImage)


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductCommentInline, ProductRatingInline]
    list_display = ['name', 'add_date', 'average_rating', 'price']

    class Meta:
        model = Product


admin.site.register(Product, ProductAdmin)

admin.site.register(ProductRating)