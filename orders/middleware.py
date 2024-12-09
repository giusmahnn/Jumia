import logging
from .models import Cart, Product, CartItem

logger = logging.getLogger(__name__)

class MergeCartSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Pre-process: Handle cart merging for authenticated users
        if request.user.is_authenticated and 'cart' in request.session:
            self.merge_session_cart_to_user_cart(request)

        response = self.get_response(request)

        # Post-process: Additional response modifications can go here (if needed)

        return response

    def merge_session_cart_to_user_cart(self, request):
        session_cart = request.session.get('cart', {})

        if not isinstance(session_cart, dict):
            logger.warning("Invalid session cart structure. Expected a dictionary.")
            return

        try:
            user_cart, created = Cart.objects.get_or_create(user=request.user)

            # Fetch products in bulk
            product_ids = session_cart.keys()
            products = Product.objects.filter(id__in=product_ids)
            product_map = {product.id: product for product in products}

            for product_id, quantity in session_cart.items():
                product = product_map.get(int(product_id))
                if product:
                    cart_item, created = CartItem.objects.get_or_create(
                        cart=user_cart,
                        product=product,
                        defaults={'quantity': quantity}
                    )
                    if not created:
                        cart_item.quantity += quantity
                        cart_item.save()
                else:
                    logger.warning(f"Product with ID {product_id} does not exist.")

            # Clear session cart after merging
            del request.session['cart']
            request.session.modified = True

        except Exception as e:
            logger.error(f"Error merging session cart: {e}")
