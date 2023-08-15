from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse


class TestAuthCustomer(TestCase):
    def setUp(self):
        self.client = Client()

        self.customer = get_user_model().objects.create(email="customer@customer.com")
        self.customer.set_password("11111111")
        self.customer.save()

        self.manager = get_user_model().objects.create(email="manager@manager.com", is_staff=True)
        self.manager.set_password("22222222")
        self.manager.save()

    def test_user_login_wrong_email(self):
        customer_login = self.client.login(email="wrong_email", password="11111111")
        self.assertFalse(customer_login)

    def test_user_login_wrong_password(self):
        customer_login = self.client.login(email="customer@customer.com", password="33333333")
        self.assertFalse(customer_login)

    def test_user_acces_admin_panel(self):
        self.client.force_login(self.customer)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_manager_acces_admin_panel(self):
        self.client.force_login(self.manager)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
