from django.shortcuts import render
from rest_framework import generics
from .models import JobApproach
from .serializers import JobSearchSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.mail import EmailMessage
from rest_framework import status
from django.conf import settings

# Create your views here.
class JobSearchListCreate(generics.ListCreateAPIView):
    queryset = JobApproach.objects.all()
    serializer_class = JobSearchSerializer
    
        
class SendFileEmail(APIView):
    
    def post(self, request):
        pdf_file = request.FILES.get("pdf_file")
        if not pdf_file:
            return Response({"error": "No file uploaded"}, status=status.HTTP_400_BAD_REQUEST)

        email = EmailMessage(
            subject="New Job / Company Approach",
            body="Please see the attached PDF file.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=["khenneth.alaiza@gmail.com"]
        )
        email.attach(pdf_file.name, pdf_file.read(), pdf_file.content_type)
        email.send()  

        return Response({"message": "Email sent successfully"}, status=status.HTTP_200_OK)