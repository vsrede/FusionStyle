# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from shop.models import Order
#
#
# @receiver(post_save, sender=Order)
# def remove_cart_items(sender, instance, **kwargs):
#     if instance.status == Order.ORDER_STATUS.COMPLETED:
#         instance.cart.cart_items.all().delete()
