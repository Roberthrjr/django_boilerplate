from django.urls import path
from .views import (
    ProductView,
    ProductCreateView,
    ProductUploadImageView,
    ProductUpdateView,
    ProductDeleteView,
    SaleCreateView,
    SaleView,
    SaleUpdateView,
    SaleDeleteView
)

urlpatterns = [
    path('products/all', ProductView.as_view()),
    path('products/create', ProductCreateView.as_view()),
    path('products/upload-image', ProductUploadImageView.as_view()),
    path('products/update/<int:pk>', ProductUpdateView.as_view()),
    path('products/delete/<int:pk>', ProductDeleteView.as_view()),
    path('sales/all', SaleView.as_view()),
    path('sales/create', SaleCreateView.as_view()),
    path('sales/update/<int:pk>', SaleUpdateView.as_view()),
    path('sales/delete/<int:pk>', SaleDeleteView.as_view()),
]