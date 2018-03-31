from django.test import TestCase
from django.contrib.auth.models import User

from product.models import Product, ProductInCart
from .models import Order, ProductInOrder


class OrderTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john',
                                             email='jlennon@beatles.com',
                                             password='glassonion')
        self.order = Order.objects.create(
            user=self.user,
            first_name='ftest',
            last_name='ltest',
            phone_nmb='12345',
            address='Dubno'
        )
        for i in range(10):
            name = 'test' + str(i)
            self.product = Product.objects.create(name=name, price=i*123)
            self.product_in_cart = ProductInCart.objects.create(product=self.product, user=self.user, pcs=1)
            self.product_in_order = ProductInOrder.objects.create(order=self.order, product=self.product, pcs=1)
        self.not_active_prod = Product.objects.create(name='not active', price=0, is_active=False)
        self.not_active_product_in_cart = ProductInCart.objects.create(product=self.not_active_prod,
                                                                       user=self.user, pcs=1)

    def test_order_confirm_view_user(self):
        url = '/order/confirm/'
        self.client.login(username='john', password='glassonion')
        response = self.client.get(url)
        active_product_name = self.product_in_cart.product.name
        self.assertContains(response, active_product_name)
        not_active_product_name = self.not_active_product_in_cart.product.name
        self.assertNotContains(response, not_active_product_name)
        active_products_nmb = ProductInCart.objects.filter(user=self.user, product__is_active=True).count()
        response = self.client.post(url, {
            'first_name': 'ftest',
            'last_name': 'ltest',
            'phone_nmb': '12345',
            'address': 'Dubno'
        })
        products_in_cart_nmb = ProductInCart.objects.filter(user=self.user).count()
        self.assertRedirects(response, '/order/my-order/%s/' % self.user.id)
        self.assertEqual(2, Order.objects.all().count())
        self.assertEqual(0, products_in_cart_nmb)
        order = Order.objects.all().last()
        products_in_order_nmb = order.productinorder_set.all().count()
        self.assertEqual(active_products_nmb, products_in_order_nmb)

    def test_order_list_view(self):
        self.client.login(username='john', password='glassonion')
        url = '/order/my-order/%s/' % self.user.id
        response = self.client.get(url)
        self.assertContains(response, self.order.id)
        self.assertContains(response, int(self.order.total_order_price))
        self.assertContains(response, self.order.id)

    def test_order_detail_view(self):
        self.client.login(username='john', password='glassonion')
        url = '/order/my-order/detail/%d/' % self.order.id
        response = self.client.get(url)
        self.assertContains(response, self.order.id)
        for prod_in_cart in self.order.productinorder_set.all():
            self.assertContains(response, prod_in_cart.product.name)
