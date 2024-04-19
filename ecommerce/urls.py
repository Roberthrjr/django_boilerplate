from django.urls import path
from .views import (
    ProductView,
    ProductCreateView,
    ProductUploadImageView,
    ProductUpdateView,
    ProductDeleteView
)

urlpatterns = [
    path('products/all', ProductView.as_view()),
    path('products/create', ProductCreateView.as_view()),
    path('products/upload-image', ProductUploadImageView.as_view()),
    path('products/update/<int:pk>', ProductUpdateView.as_view()),
    path('products/delete/<int:pk>', ProductDeleteView.as_view())
]