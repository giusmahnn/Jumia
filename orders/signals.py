# from django.contrib.auth.signals import user_logged_in
# from django.dispatch import receiver
# from .models import Cart, CartItem, Product

# @receiver(user_logged_in)
# def merge_session_cart(sender, request, user, **kwargs):
#     if 'cart' in request.session:
#         session_cart = request.session.get('cart', {})
#         user_cart, created = Cart.objects.get_or_create(user=user)

#         for product_id, quantity in session_cart.items():
#             product = Product.objects.get(id=product_id)
#             cart_item, created = CartItem.objects.get_or_create(
#                 cart=user_cart,
#                 product=product,
#                 defaults={'quantity': quantity}
#             )
#             if not created:
#                 cart_item.quantity += quantity
#                 cart_item.save()

#         # Clear the session cart after merging
#         del request.session['cart']
#         request.session.modified = True
