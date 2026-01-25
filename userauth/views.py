from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.forms.models import model_to_dict
from .models import User
from .serializers import UserSerializer, EmailTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics
from rest_framework.permissions import AllowAny
from .models import EmailVerification
from utils.email import send_verification_email
from rest_framework_simplejwt.authentication import JWTAuthentication
import json
from rest_framework.pagination import PageNumberPagination


class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer


# class ProtectedView(APIView):
#     permission_classes = [IsAuthenticated]
    
#     def get(self, request):
#         return Response({
#             'message': 'This is a protected endpoint',
#             'user': request.user.username
#         })


class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"error": "Refresh token is required"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            return Response(
                {"message": "Successfully logged out"},
                status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
            
class GetData(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({
            'message': 'This is a protected endpoint',
            'user': serializer.data
        })
        
class ListCreateWithAuth(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class ListCreate(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def perform_create(self, serializer):
        user = serializer.save()
        verification = EmailVerification.objects.create(user=user)
        send_verification_email(user, verification.token)
    
class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class AddSuperAdmin(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        
        data = UserSerializer(data=request.data)
        if data.is_valid():
            data.save()
            return Response(data.data, status=status.HTTP_201_CREATED)
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
    
class VerifyEmail(APIView):
    def get(self, request, token):
        try:
            verification = EmailVerification.objects.get(token=token)
            user = verification.user
            user.is_active = True
            user.is_email_verified = True
            user.save()

            verification.delete()

            return Response({"message": "Email verified successfully"})
        except EmailVerification.DoesNotExist:
            return Response(
                {"error": "Invalid or expired token"},
                status=status.HTTP_400_BAD_REQUEST
                
            )
class CheckEmailIfExist(APIView):
    def get(self, request, email):
        user = User.objects.filter(email=email).first()
        if user:
            return Response({"exists": True})
        else:
            return Response({"exists": False})
    


from utils.translator import translate_text


class TestTranslate(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        
        
        text = request.data["q"]
        source = request.data["source"]
        target = request.data["target"]
        

        result = translate_text(text, source, target)

        return Response({
            "translatedText": result
        })
        
from rest_framework.parsers import MultiPartParser, FormParser

class UpdateUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        user = generics.get_object_or_404(User, pk=pk)

        serializer = UserSerializer(
            user,
            data=request.data,
            partial=True,
            context={"request": request}  
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)
        
class UpdateUserNotEmployee(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request):

        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True,
            context={"request": request}  
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)
    

class DynamicPageSizePagination(PageNumberPagination):
    
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
import json

class GetAllUserByFilter(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = UserSerializer
    pagination_class = DynamicPageSizePagination

    def post(self, request):
        page_size = request.query_params.get('page_size', 10)

        try:
            page_size = int(page_size)
            if page_size > 100:
                page_size = 100
            if page_size < 1:
                page_size = 10
        except ValueError:
            page_size = 10

        filter_list = request.data.get('filter')

        if not filter_list:
            users = User.objects.all()
        else:
            if isinstance(filter_list, str):
                filter_list = json.loads(filter_list)

            allowed_filters = ['role', 'is_active']

            filters = {
                key: filter_list[key]
                for key in allowed_filters
                if key in filter_list
            }

            users = User.objects.filter(**filters)

        paginator = DynamicPageSizePagination()
        paginator.page_size = page_size

        paginated_users = paginator.paginate_queryset(users, request)

        serializer = UserSerializer(paginated_users, many=True)

        return paginator.get_paginated_response(serializer.data)






           






        

        

    


