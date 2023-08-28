from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.status import (HTTP_200_OK, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND,
                                   HTTP_405_METHOD_NOT_ALLOWED)
from rest_framework.test import APIClient, APITestCase

from shop.models import Brand, Category, Product
from utils.samples import sample_brand, sample_category, sample_product


class TestAPI(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.category = sample_category(name="TestCategory", description="Category Description")
        self.brand = sample_brand(name="TestBrand", description="Brand Description")
        self.user = get_user_model().objects.create(email="test_api@example.com")
        self.user.set_password("qwerty1234")
        self.user.save()

    def test_product_details(self):
        self.client.force_authenticate(user=self.user)
        self.product = sample_product(
            name="Test Product",
            price=100.00,
            category=self.category,
            brand=self.brand,
        )

        result = self.client.get(reverse("api:product_detail", kwargs={"pk": self.product.pk}))
        self.assertEqual(result.status_code, HTTP_200_OK)
        self.assertEqual(
            result.data,
            {
                "name": "Test Product",
                "price": "100.00",
                "category": 1,
                "brand": 1,
                "title": "Sample Product Title",
                "description": "Sample Product Description",
            },
        )

    def test_delete_product(self):
        self.client.force_authenticate(user=self.user)
        product = sample_product(category=self.category, brand=self.brand)

        response = self.client.delete(reverse("api:product_delete", kwargs={"pk": product.id}))
        self.assertEqual(response.status_code, HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.count(), 0)

    def test_update_product(self):
        self.client.force_authenticate(user=self.user)
        product = sample_product(category=self.category, brand=self.brand)

        data = {
            "name": "Updated Product",
            "price": "199.99",
            "category": self.category.id,
            "brand": self.brand.id,
            "title": "Updated Product Title",
            "description": "Updated Product Description",
        }

        response = self.client.put(reverse("api:product_update", kwargs={"pk": product.id}), data, format="json")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(Product.objects.get(id=product.id).name, "Updated Product")

    def test_delete_product_not_found(self):
        self.client.force_authenticate(user=self.user)

        invalid_product_id = 99999
        response = self.client.delete(reverse("api:product_delete", kwargs={"pk": invalid_product_id}))
        self.assertEqual(response.status_code, HTTP_404_NOT_FOUND)

    def test_create_product_invalid_data(self):
        self.client.force_authenticate(user=self.user)

        data = {
            "name": "",
            "price": "199.99",
            "category": self.category.id,
            "brand": self.brand.id,
            "title": "Updated Product Title",
            "description": "Updated Product Description",
        }

        response = self.client.post(reverse("api:product_create"), data, format="json")
        self.assertEqual(response.status_code, HTTP_400_BAD_REQUEST)

    def tearDown(self):
        Product.objects.all().delete()
        Category.objects.all().delete()
        Brand.objects.all().delete()
