from django.contrib.auth.models import User
from django.test import TestCase
from .models import ProductRating, Product, ProductInCart
from .views import PRODUCTS_ON_PAGE


class ProductTest(TestCase):
    def setUp(self):
        for i in range(10):
            name = 'test' + str(i)
            self.product = Product.objects.create(name=name, price=i*123)
        self.not_active_prod = Product.objects.create(name='not active', price=0, is_active=False)

        self.user = User.objects.create_user(username='john',
                                            email='jlennon@beatles.com',
                                            password='glassonion')

    def test_rating_signal(self):
        user1 = User.objects.create_user(username='john1',
                                        email='jlennon@beatles.com',
                                        password='glassonio')
        rating = ProductRating.objects.create(product=self.product, rating=5, user=self.user)
        rating1 = ProductRating.objects.create(product=self.product, rating=0, user=user1)
        avg = (rating.rating + rating1.rating)/self.product.productrating_set.all().count()
        self.assertEqual(self.product.average_rating, avg)

    def test_product_detail_view(self):
        url = '/product/detail/%s/' % self.product.id
        self.assertEqual(url, self.product.get_absolute_url())
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_main_page_view(self):
        response = self.client.get('/')
        for pr in Product.objects.all().order_by('name')[:PRODUCTS_ON_PAGE]:
            if pr.is_active:
                self.assertContains(response, pr.name)
            else:
                self.assertNotContains(response, pr.name)

    def test_nmb_of_product_rating(self):
        user1 = User.objects.create_user(username='john1',
                                        email='jlennon@beatles.com',
                                        password='glassonio')
        rating = ProductRating.objects.create(product=self.product, rating=5, user=self.user)
        rating1 = ProductRating.objects.create(product=self.product, rating=0, user=user1)
        nmb_rating = ProductRating.objects.filter(product=self.product).count()
        self.assertEqual(nmb_rating, self.product.get_nmb_of_rating())


class ProductInCartTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='john',
                                            email='jlennon@beatles.com',
                                            password='glassonion')
        self.first_product = Product.objects.create(name='first', price=10)
        self.second_product = Product.objects.create(name='second', price=20)
        self.third_product = Product.objects.create(name='third', price=30)
        self.first_product_in_cart = ProductInCart.objects.create(product=self.first_product, user=self.user, pcs=1)
        self.second_product_in_cart = ProductInCart.objects.create(product=self.second_product, user=self.user, pcs=2)
        self.third_product_in_cart = ProductInCart.objects.create(product=self.third_product, user=self.user, pcs=3)

    def test_product_in_cart_save(self):
        pcs = 2
        nmb_of_product_in_cart = ProductInCart.objects.all().count()
        pcs_first = self.first_product_in_cart.pcs
        test_product_in_cart = ProductInCart(product=self.first_product, user=self.user, pcs=pcs)
        test_product_in_cart.save()
        pcs_last = ProductInCart.objects.get(user=self.user, product=self.first_product).pcs
        self.assertEqual(pcs_first+pcs, pcs_last)
        self.assertEqual(nmb_of_product_in_cart, ProductInCart.objects.all().count())


class ProductCommentTest(TestCase):
    def test_comment_view(self):
        product = Product.objects.create(name='first', price=10)
        user = User.objects.create_user(username='john',
                                            email='jlennon@beatles.com',
                                            password='glassonion')
        self.client.login(username='john', password='glassonion')
        comment = "some comment"
        response = self.client.post('/product/comments/%d/' % product.id, {'text': comment})
        self.assertRedirects(response, product.get_absolute_url())
        self.assertEqual(product.productcomment_set.all().count(), 1)
        response = self.client.get('/product/detail/%d/' % product.id)
        self.assertContains(response, comment)


class ProductInCartTest(TestCase):
    def test_add_product_in_cart(self):
        product = Product.objects.create(name='first', price=10)
        user = User.objects.create_user(username='john',
                                            email='jlennon@beatles.com',
                                            password='glassonion')
        self.client.login(username='john', password='glassonion')
        pcs = 10
        response = self.client.post('/product/add_product_in_cart/%d/' % product.id, {'pcs': pcs})
        self.assertRedirects(response, product.get_absolute_url())
        self.assertEqual(ProductInCart.objects.all().count(), 1)
        response = self.client.get('/product/product_in_cart/')
        self.assertContains(response, product.name)

