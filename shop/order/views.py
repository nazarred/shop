from django.contrib import messages
from django.urls import reverse
from django.views.generic import CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


from product.models import ProductInCart
from .forms import OrderModelForm
from .models import Order


class OrderConfirmView(CreateView):
    form_class = OrderModelForm
    template_name = 'order/confirm_order.html'

    def get_success_url(self):
        return reverse('order:user_orders', kwargs={'pk': self.request.user.id})

    def get_form_kwargs(self):
        kwargs = super(OrderConfirmView, self).get_form_kwargs()
        if self.request.user.is_authenticated:
            kwargs['initial'] = {
                'last_name': self.request.user.last_name,
                'first_name': self.request.user.first_name,
                'phone_nmb': self.request.user.profile.phone_nmb
            }
        return kwargs

    def get_active_products_in_cart(self):
        products = ProductInCart.objects.user_cart(self.request, is_active=True).select_related('product',
                                                                                                "user")
        return products

    def form_valid(self, form):
        order = form.save(commit=False)
        if self.request.user.is_authenticated:
            order.user = self.request.user
        order = form.save()
        order.products.add(*[product for product in self.get_active_products_in_cart()])
        ProductInCart.objects.user_cart(self.request, is_active=False).delete()
        messages.success(self.request, 'Order created')
        return super(OrderConfirmView, self).form_valid(form)


class UserOrdersView(LoginRequiredMixin, ListView):
    form_class = OrderModelForm
    template_name = 'order/user_orders.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class UserOrderDetailView(DetailView):
    model = Order
    template_name = 'order/user_orders_detail.html'
