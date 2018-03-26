from django.test import TestCase
from django.contrib.auth.models import User

from product.models import Product, ProductInCart
from .models import Order


class OrderTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john',
                                             email='jlennon@beatles.com',
                                             password='glassonion')
        for i in range(10):
            name = 'test' + str(i)
            self.product = Product.objects.create(name=name, price=i*123)
            self.product_in_cart = ProductInCart.objects.create(product=self.product, user=self.user, pcs=1)
        self.not_active_prod = Product.objects.create(name='not active', price=0, is_active=False)
        self.not_active_product_in_cart = ProductInCart.objects.create(product=self.not_active_prod,
                                                                       user=self.user, pcs=1)

    def test_order_model(self):
        order = Order.objects.create(
            user=self.user,
            first_name='ftest',
            last_name='ltest',
            phone_nmb='12345',
            address='Dubno'
        )

        product_in_cart_list = list(ProductInCart.objects.filter(user=self.user, product__is_active=True))
        order.products.add(*product_in_cart_list)
        order_price = order.get_total_price()
        product_in_cart_price = 0
        for prod in ProductInCart.objects.filter(user=self.user, product__is_active=True):
            product_in_cart_price += prod.get_total_product_price
        self.assertEqual(order_price, product_in_cart_price)

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
        products_in_cart_nmb = ProductInCart.objects.filter(user=self.user, in_order=False).count()
        self.assertRedirects(response, '/order/my-order/%s/' % self.user.id)
        self.assertEqual(1, Order.objects.all().count())
        self.assertEqual(0, products_in_cart_nmb)
        order = Order.objects.get(user=self.user)
        products_in_order_nmb = order.products.all().count()
        self.assertEqual(active_products_nmb, products_in_order_nmb)

    def test_order_list_view(self):
        self.client.login(username='john', password='glassonion')
        url = '/order/my-order/%s/' % self.user.id
        order = Order.objects.create(
            user=self.user,
            first_name='ftest',
            last_name='ltest',
            phone_nmb='12345',
            address='Dubno'
        )

        product_in_cart_list = list(ProductInCart.objects.filter(user=self.user, product__is_active=True))
        order.products.add(*product_in_cart_list)
        response = self.client.get(url)
        self.assertContains(response, order.id)
        self.assertContains(response, int(order.get_total_price()))

    def test_order_detail_view(self):
        self.client.login(username='john', password='glassonion')
        order = Order.objects.create(
            user=self.user,
            first_name='ftest',
            last_name='ltest',
            phone_nmb='12345',
            address='Dubno'
        )
        product_in_cart_list = list(ProductInCart.objects.filter(user=self.user, product__is_active=True))
        order.products.add(*product_in_cart_list)
        url = '/order/my-order/detail/%d/' % order.id
        response = self.client.get(url)
        self.assertContains(response, order.id)
        for prod_in_cart in product_in_cart_list:
            self.assertContains(response, prod_in_cart.product.name)
