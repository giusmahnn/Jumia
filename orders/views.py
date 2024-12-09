from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from .serializers import *
from .models import *   

# Create your views here.

class CartView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            cart, created  = Cart.objects.get_or_create(user=request.user)
        else:
            session_cart = request.session.get('cart', {})
            return Response(session_cart, status.HTTP_200_OK)
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def delete(self, request):
        if request.user.is_authenticated:
            cart = get_object_or_404(Cart, user=request.user)
            cart.cart_items.all().delete()
        else:
            cart_session = request.session['cart'] = {}
        return Response({"Message":"Cart deleted successfully"}, status=status.HTTP_204_NO_CONTENT)



class CartItemView(APIView):
    def post(self, request):
        product_id = request.data.get("product")
        quantity = request.data.get('quantity', 1)

        # if user is authenticated
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
            product = get_object_or_404(Product, id=product_id)
            cart_item, created = CartItem.objects.get_or_create(cart=cart,
                                                                product=product,
                                                                default={"quantity": quantity}
                                                                )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
        else:
            # For annonymous users
            session_cart, created = request.session.get('cart', {})
            session_cart[product_id] = session_cart.get(product_id) + quantity
            request.session["cart"] = session_cart
            request.session.modified = True
        return Response({"Message": "Item added to cart"}, status.HTTP_201_CREATED)
    
    def delete(self, request, pk):
        if request.user.is_autenticated:
            cart = get_object_or_404(Cart, user=request.user)
            cart_item = get_object_or_404(CartItem, id=pk, cart=cart)
            cart_item.delete()

        else:
            session_cart = request.session.get(cart,{})
            session_cart.pop(str(pk), None)
            request.session["cart"] = session_cart
            request.session.modified = True

        return Response({"Message": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)



class CheckoutView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            cart = get_object_or_404(cart, user=request.user)
            if not cart.cart_items.exists():
                return Response({"Message": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
            
            order = Order.objects.create(customer=request.user,
                                        vendor=cart.cart_items.first().product.vendor,
                                        status='Pending'
                                        )
            for cart_item in cart.cart_items.all():
                OrderItem.objects.create(order=order,
                                        product=cart_item.product,
                                        quantity=cart_item.quantity
                                        )
                cart.cart_items.all().delete()

                serializer = ShippingAddressSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save(order=order, customer=request.user)
                    return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        else:
            return Response({"Message": "Login is required to checkout the order"}, status.HTTP_401_UNAUTHORIZED)