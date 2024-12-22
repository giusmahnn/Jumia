from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db import transaction
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
    permission_classes = [AllowAny]
    def post(self, request):
        product_id = request.data.get('product')
        quantity = request.data.get('quantity', 1)

        if request.user.is_authenticated:
            # Handle authenticated user's cart
            cart, created = Cart.objects.get_or_create(user=request.user)
            product = get_object_or_404(Product, id=product_id)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart, product=product, defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
        else:
            # Handle anonymous user's cart
            session_cart = request.session.get('cart', {})
            session_cart[product_id] = session_cart.get(product_id, 0) + quantity
            request.session['cart'] = session_cart
            request.session.modified = True

        return Response({"message": "Item added to cart"}, status=status.HTTP_201_CREATED)




class CartItemDeleteView(APIView):
    permission_classes = [AllowAny]
    def delete(self, request, pk):
        if request.user.is_authenticated:
            cart = get_object_or_404(Cart, user=request.user)
            cart_item = get_object_or_404(CartItem, pk=pk, cart=cart)
            cart_item.delete()

        else:
            session_cart = request.session.get(cart,{})
            session_cart.pop(str(pk), None)
            request.session["cart"] = session_cart
            request.session.modified = True

        return Response({"Message": "Item removed from cart"}, status=status.HTTP_204_NO_CONTENT)



# class CheckoutView(APIView):
#     def post(self, request):
#         if request.user.is_authenticated:
#             cart = get_object_or_404(Cart, user=request.user)
#             if not cart.cart_items.exists():
#                 return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)

#             # Create the order
#             order = Order.objects.create(
#                 customer=request.user,
#                 vendor=cart.cart_items.first().product.vendor,  # correct this line
#                 status='pending'
#             )

#             # Create order items
#             for item in cart.cart_items.all():
#                 OrderItem.objects.create(
#                     order=order,
#                     product=item.product,
#                     quantity=item.quantity,
#                 )

#             # Clear the cart after checkout
#             cart.cart_items.all().delete()
#             serializers  = ShippingAddressSerializer(data=request.data)
#             if serializers.is_valid():
#                 serializers.save(order=order,customer=request.user)
#                 return Response({"message": "Checkout successful"}, status=status.HTTP_200_OK)

#             return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
#         else:
#             return Response({"error": "Login required for checkout"}, status=status.HTTP_401_UNAUTHORIZED)





class CheckoutView(APIView):
    @transaction.non_atomic_requests
    def post(self, request):

        if request.user.is_authenticated:
            cart = get_object_or_404(Cart, user=request.user)
            if not cart.cart_items.exists():
                return Response({"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST)
            
            # create shipping address
            print("Successfully created shipping address")
            serializers = ShippingAddressSerializer(data=request.data)
            if serializers.is_valid():
                serializers.save(user=request.user)
                
            print("This is a pending order")
            order = Order.objects.create(
                customer=request.user,
                vendor=cart.cart_items.first().product.vendor,  # correct this line
                status='pending'
            )  
            
            # create Order
            print("This order quantity")
            for item in cart.cart_items.all():
                order_items = OrderItem.objects.create(
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
                order.items.add(order_items)

            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Login required for checkout"}, status=status.HTTP_401_UNAUTHORIZED)