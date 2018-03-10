from django.contrib import admin
from .models import Product, ProductRating, ProductComment, ProductImage, ProductInCart


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
    list_filter = ['add_date', 'name']

    class Meta:
        model = Product

    def get_form(self, request, obj=None, **kwargs):
        form = super(ProductAdmin, self).get_form(request, obj, **kwargs)
        if obj and 'main_image' in form.base_fields:
            form.base_fields['main_image'].queryset = obj.images.all()
        return form

    def get_fields(self, request, obj=None):
        fields = super(ProductAdmin, self).get_fields(request, obj)
        if not obj:
            fields.remove('main_image')
        return fields


admin.site.register(Product, ProductAdmin)

admin.site.register(ProductRating)

admin.site.register(ProductInCart)
