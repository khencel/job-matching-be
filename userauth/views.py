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
from utils.helper import paginate_queryset
from .serializers import ForgotPasswordSerializer, ResetPasswordSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from django.core.mail import send_mail


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
        context_text = json.loads(self.request.data.get('context'))
        
        verification = EmailVerification.objects.create(user=user)
        send_verification_email(user, verification.token, context_text)
    
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

from django.shortcuts import redirect
class VerifyEmail(APIView):
    def get(self, request, token):
        try:
            verification = EmailVerification.objects.get(token=token)
            user = verification.user
            user.is_active = True
            user.is_email_verified = True
            user.save()

            verification.delete()
            return redirect(settings.FRONTEND_URL+"login")
            # return Response({"message": "Email verified successfully"})
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
    
class GetAllUserByFilter(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        role = request.data['role']

        if role == "all":
            user = User.objects.all()
        else:
            user = User.objects.filter(role=role)
        
        
        return paginate_queryset(
            request,
            user,
            UserSerializer
        )
    
    
class UpdateEmployerDetails(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def put(self, request, pk):
        emp = User.objects.get(pk=pk)
        details = request.data.get('details', {}) 
        emp.userDetails_emp = json.loads(details)
        emp.save()
        serializer = UserSerializer(emp)
        return Response(serializer.data)


class ShowAllCompany(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        company = User.objects.filter(role="employer").values("userDetails_emp")
        return Response(company)


from django.core.mail import send_mail
from django.conf import settings

class TestApi(APIView):
    
    def get(self, request):
        try:
            send_mail(
                subject='Test Email',
                message='Hello! Gumagana na ang email sending 🎉',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['khenneth.alaiza@gmail.com'],
                fail_silently=False,
            )
            return Response({"status": "success", "message": "Email sent successfully"})
        except Exception as e:
            return Response({"status": "error", "error": str(e)})
    
class ChangeStatusUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        user = generics.get_object_or_404(User, pk=pk)
        user.is_active = not user.is_active
        user.save()
        return Response("success")
    

class CheckUserPassword(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")

        if not current_password or not new_password:
            return Response(
                {"message": "current_password and new_password are required"}
            )

        user = request.user  

      
        if not user.check_password(current_password):
            return Response(
                {"value":False,"message": "Password is incorrect"}
            )


        user.set_password(new_password)
        user.save()

        return Response(
            {
                "value":True,
                "message": "Password successfully changed"
            },
            status=status.HTTP_200_OK
        )

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
        
class ContactUsEmail(APIView):
    def post(self, request):
        data = request.data
        try:
            # Render HTML template with payload
            email_html = render_to_string('contact_us/contact_email.html', data)

            # Prepare EmailMessage
            email = EmailMessage(
                subject=f"Contact Us: {data.get('subject')}",
                body=email_html,
                from_email=data['email'],
                to=[settings.DEFAULT_FROM_EMAIL] 
            )
            email.content_subtype = "html" 
            email.send()  # send email

            return Response({"message": "Email sent successfully!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


   
from django.utils import timezone
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives

token_generator = PasswordResetTokenGenerator()   
        
class ForgotPassword(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"].strip()

        generic_ok = {
            "message": "If that email exists, we sent a password reset link."
        }

        user = User.objects.filter(
            email__iexact=email,
            is_active=True
        ).first()

        # 🔒 Do not reveal if user exists
        if not user:
            return Response(generic_ok, status=status.HTTP_200_OK)

        # Generate token
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)

        # Frontend reset URL
        frontend_url = getattr(settings, "FRONTEND_RESET_PASSWORD_URL", None)
        if not frontend_url:
            frontend_url = getattr(settings, "FRONTEND_URL", "").rstrip("/") + "/forgot-password"

        reset_link = f"{frontend_url}?uid={uidb64}&token={token}"

        subject = "Reset Your Password"
        from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@example.com")

        # Render HTML template
        html_content = render_to_string(
            "emails/reset_password.html",
            {
                "reset_link": reset_link,
                "user_email": user.email,
                "year": timezone.now().year,
            },
        )

        text_content = strip_tags(html_content)

        # Send email (HTML + text)
        email_message = EmailMultiAlternatives(
            subject,
            text_content,
            from_email,
            [user.email],
        )

        email_message.attach_alternative(html_content, "text/html")
        email_message.send()

        return Response(generic_ok, status=status.HTTP_200_OK)
        
        
class ResetPassword(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        uidb64 = serializer.validated_data["uidb64"]
        token = serializer.validated_data["token"]
        new_password = serializer.validated_data["new_password"]

        # decode uid
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid, is_active=True)
        except Exception:
            return Response({"message": "Invalid reset link."}, status=status.HTTP_400_BAD_REQUEST)

        # check token
        if not token_generator.check_token(user, token):
            return Response({"message": "Reset link expired or invalid."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save(update_fields=["password"])

        return Response({"message": "Password has been reset successfully."}, status=status.HTTP_200_OK)




           






        

        

    


