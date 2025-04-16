from django.urls import path
from .views import *

urlpatterns = [
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/item/', CartItemView.as_view(), name='cart_item'),
    path('cart/item/<int:pk>/', CartItemDeleteView.as_view(), name='cart_item_delete'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order/history', OrderHistoryView.as_view(), name='order_history'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    # path('order/<int:pk>/cancel/', OrderCancelView.as_view(), name='order_cancel'),
    # path('order/<int:pk>/return/', OrderReturnView.as_view(), name='order_return'),
    # path('order/<int:pk>/track/', OrderTrackView.as_view(), name='order_track'),
    # path('order/<int:pk>/invoice/', OrderInvoiceView.as_view(), name='order_invoice'),
    # path('order/<int:pk>/invoice/download/', OrderInvoiceDownloadView.as_view(), name='order_invoice_download'),
    # path('order/<int:pk>/invoice/send/', OrderInvoiceSendView.as_view(), name='order_invoice_send'),
    # path('order/<int:pk>/invoice/print/', OrderInvoicePrintView.as_view(), name='order_invoice_print'),
]
