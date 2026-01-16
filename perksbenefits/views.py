from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import PerksBenefits
from .serializers import PerksBenefitsSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

# Create your views here.



class PerksBenefitsListCreate(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PerksBenefits.objects.all()
    serializer_class = PerksBenefitsSerializer
    def get_queryset(self):
        return PerksBenefits.objects.filter(user=self.request.user, deleted=False)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
class PerksBenefitsRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = PerksBenefits.objects.all()
    serializer_class = PerksBenefitsSerializer
    

    