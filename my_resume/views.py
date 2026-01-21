from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import MyResumeSerializer
from .models import MyResume



class CreateResumeView(APIView):
    authentication_classes = [JWTAuthentication]
    def post(self, request):
        resume = MyResume.objects.filter(user=request.user).first()
        
        serializer = MyResumeSerializer(
            instance=resume, 
            data=request.data
        )
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=200 if resume else 201)

        return Response(serializer.errors, status=400)