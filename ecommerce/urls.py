# Importamos la funcion path del modulo django.urls para definir las rutas
from django.urls import path
# Importamos las vistas del directorio actual
from .views import (
    RegisterView,
    LoginView,
    ProductView,
    ProductCreateView,
    ProductUploadImageView,
    ProductUpdateView,
    ProductDeleteView,
    SaleCreateView,
    SaleView,
    SaleUpdateView,
    SaleDeleteView,
    CreateInvoiceView,
    GetInvoiceView,
    CreatePaymentView,
    NotificationPaymentView
)

# Definimos las rutas
urlpatterns = [
    path('user/register', RegisterView.as_view()),
    path('user/login', LoginView.as_view()),
    path('products/all', ProductView.as_view()),
    path('products/create', ProductCreateView.as_view()),
    path('products/upload-image', ProductUploadImageView.as_view()),
    path('products/update/<int:pk>', ProductUpdateView.as_view()),
    path('products/delete/<int:pk>', ProductDeleteView.as_view()),
    path('sales/all', SaleView.as_view()),
    path('sales/create', SaleCreateView.as_view()),
    path('sales/update/<int:pk>', SaleUpdateView.as_view()),
    path('sales/delete/<int:pk>', SaleDeleteView.as_view()),
    path('invoice/create', CreateInvoiceView.as_view()),
    path('invoice/get/<int:tipo_de_comprobante>/<str:serie>/<int:numero>', GetInvoiceView.as_view()),
    path('payment/create', CreatePaymentView.as_view()),
    path('payment/notification', NotificationPaymentView.as_view())
]