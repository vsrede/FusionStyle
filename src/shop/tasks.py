from celery import shared_task

from shop.models import Brand, Category, Product


@shared_task
def generate_product_brand_category():
    Category.generate_instances()
    Brand.generate_instances()
    Product.generate_instances()
