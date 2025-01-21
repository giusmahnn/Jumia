from rest_framework.response import Response
from django.conf import settings 
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated

from accounts.permissions import IsAdmin
from .serializers import *
from accounts.utils import *
from accounts.models import *
from rest_framework.views import APIView
from products.pagination import CustomPagination
from django.db.models import Sum, Avg
# Create your views here.



class VendorCreateView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VendorSerializer(data=request.data)
        
        # Validate the serializer
        if serializer.is_valid():
            user = serializer.save()
            user.user.otp = generate_otp()
            user.save()

            # Prepare email context
            context = {
                "name": user.user.first_name,
               "verify_link": request.build_absolute_uri(user.get_absolute_url()),
                "subject": "Verify your Jumia account"
            }

            # Render email template and send email
            template = render_to_string("accounts/verify-email.html", context)
            send_email(user.user.email, "Verify Your Account", template)

            # Prepare response data
            data = {
                "Message": "Account Created Successfully",
                "Vendor_info": VendorSerializer(user).data,
                "Token": jwt_auth(user)
            }

            return Response(data, status=status.HTTP_201_CREATED)
        
        # Handle validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class VendorLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = VendorLoginSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            vendor_user = serializer.validated_data['user']  # Get the Account instance
            vendor = vendor_user.vendor # Get the Vendor instance through the Vendor instance attribute related
            data = {
                "Vendor_info": VendorSerializer(vendor).data,
                "Token": jwt_auth(vendor_user)
            }
            return Response(data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class CreateProduct(APIView):
    permission_classes = [IsAdmin, IsAuthenticated]
    def get(self, request):
        data = {}
        try:
            # Fetch all products created by the authenticated vendor
            product = Product.objects.filter(vendor=self.request.user.vendor)
            paginator = CustomPagination()
            paginate_products = paginator.paginate_queryset(product, request)
            data["Products"] = VendorProductSerializer(paginate_products, many=True).data
        except Product.DoesNotExist:
            return Response({"message": "No Products"}, status=status.HTTP_404_NOT_FOUND)
        return paginator.get_paginated_response(data)
    
    def post(self, request):
        serializers = VendorProductSerializer(data=request.data)
        data = {}
        if serializers.is_valid():
            product = serializers.save(vendor=request.user.vendor)
            data["Product"] = VendorProductSerializer(product).data
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    


class VendorDashboardView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]
    def get(self, request):
        vendor = request.user.vendor

        total_products = vendor.products.count()
        total_sales = vendor.vendor_orders.filter(status='Completed').count()
        total_orders = vendor.vendor_orders.count()
        total_revenue = vendor.vendor_orders.filter(status='Completed').aggregate(Sum('price'))['price__sum'] or 0
        # average_rating = vendor.reviews.aggregate(Avg('rating'))['rating__avg'] or 0

        data_dashboard = {
            "Total Products": total_products,
            "Total Sales": total_sales,
            "Total Orders": total_orders,
            "Total Revenue": total_revenue
            # "Average Rating": average_rating
        }

        return Response(data_dashboard, status=status.HTTP_200_OK)



class Delete(APIView):
    permission_classes = [AllowAny]
    def delete(self, request):
        products = Product.objects.all().delete()
        return Response({"message": "All products deleted successfully."})