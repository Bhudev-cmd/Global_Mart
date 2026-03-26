from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Cart, CartItem, Order, OrderItem, Product, UserAddress


class StoreFlowTests(TestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='alice', password='pass12345')
		self.product = Product.objects.create(
			name='Laptop',
			description='Test product',
			price=Decimal('499.99'),
			stock=5,
			image_url='https://example.com/laptop.jpg',
		)

	def test_product_list_search_filters_results(self):
		Product.objects.create(
			name='Phone',
			description='Another product',
			price=Decimal('199.99'),
			stock=10,
			image_url='https://example.com/phone.jpg',
		)

		response = self.client.get(reverse('product_list'), {'search': 'lap'})

		self.assertEqual(response.status_code, 200)
		products = list(response.context['products'])
		self.assertEqual(len(products), 1)
		self.assertEqual(products[0].name, 'Laptop')

	def test_add_to_cart_requires_login(self):
		response = self.client.get(reverse('add_to_cart', args=[self.product.id]))
		self.assertEqual(response.status_code, 302)
		self.assertIn('/accounts/login/', response.url)

	def test_add_to_cart_twice_increases_quantity(self):
		self.client.login(username='alice', password='pass12345')

		self.client.get(reverse('add_to_cart', args=[self.product.id]))
		self.client.get(reverse('add_to_cart', args=[self.product.id]))

		cart = Cart.objects.get(user=self.user)
		cart_item = CartItem.objects.get(cart=cart, product=self.product)
		self.assertEqual(cart_item.quantity, 2)

	def test_payment_redirects_to_add_address_when_missing(self):
		self.client.login(username='alice', password='pass12345')
		self.client.get(reverse('add_to_cart', args=[self.product.id]))

		response = self.client.get(reverse('payment'))

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, reverse('add_address'))

	def test_payment_post_creates_order_and_clears_cart(self):
		self.client.login(username='alice', password='pass12345')
		self.client.get(reverse('add_to_cart', args=[self.product.id]))

		UserAddress.objects.create(
			user=self.user,
			full_name='Alice User',
			phone='9999999999',
			street_address='123 Main Street',
			landmark='Near Park',
			city='Ranchi',
			state='Jharkhand',
			pin_code='834001',
			country='India',
		)

		response = self.client.post(reverse('payment'))

		self.assertEqual(response.status_code, 302)
		self.assertEqual(response.url, reverse('order_success'))

		order = Order.objects.get(user=self.user)
		order_item = OrderItem.objects.get(order=order, product=self.product)
		self.assertEqual(order.total_price, Decimal('499.99'))
		self.assertEqual(order_item.quantity, 1)
		self.assertEqual(order_item.price, Decimal('499.99'))
		self.assertFalse(CartItem.objects.filter(cart__user=self.user).exists())
