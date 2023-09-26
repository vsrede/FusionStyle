from shop.models import Cart, CartItem, GuestCart


def merge_guest_cart_with_user_cart(request, user):
    guest_session_id = request.session.get("guest_session_id")
    if guest_session_id:
        guest_cart = GuestCart.objects.filter(session_key=guest_session_id).first()
        if guest_cart:
            user_cart, created = Cart.objects.get_or_create(customer=user)

            for guest_cart_item in guest_cart.guestcartitem_set.all():
                cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=guest_cart_item.product)
                if not created:
                    cart_item.quantity += guest_cart_item.quantity
                    cart_item.save()

            guest_cart.delete()
            del request.session["guest_session_id"]
