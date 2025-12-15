from django.shortcuts import render
from rest_framework import generics
from .models import Products
from .serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class ProductListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    
    
class ProductRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
