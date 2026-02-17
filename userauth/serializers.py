
from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
import json
from perksbenefits.models import PerksBenefits
from perksbenefits.serializers import PerksBenefitsSerializer
from my_resume.models import MyResume
from job_seeker_documents.models import ApplicantDocument
from datetime import date


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False, allow_null=True)
    banner = serializers.ImageField(required=False, allow_null=True)
    perks_benefits = serializers.SerializerMethodField()
    resume = serializers.SerializerMethodField()
    documents = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email','password','deleted_at','first_name','last_name',
            'userDetails_emp','userDetails_job_seeker','userDetails_supervisory',
            'avatar','banner','role','is_email_verified','perks_benefits','is_active','created_at','resume','documents'
        ]
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'perks_benefits': {'read_only': True},
        }
        
        read_only_fields = [
            "user_id",
            "perks_benefits"
        ]
        
    def get_documents(self, obj):
        user_id = obj.id
        documents = ApplicantDocument.objects.filter(user_id=user_id, deleted=False).values('documents')
        return documents
        
        
    def get_resume(self, obj):
        user_id = obj.id
        # Renamed variable to 'resume_obj' to avoid confusion with the field 'resume'
        resume = MyResume.objects.filter(user_id=user_id, deleted=False).first()
        if resume:
            return resume.resume.name
        return None
        
    def get_perks_benefits(self, obj):
        user_id = obj.id
        perks_benefits = PerksBenefits.objects.filter(user_id=user_id, deleted=False)
        serializer = PerksBenefitsSerializer(perks_benefits, many=True)
        return serializer.data
        
    def create(self, validated_data):
        user_type = self.initial_data['user_type']
        details = self.initial_data['details']
        
        password = validated_data.pop('password', None) or 'defaultpassword123'
        first_name = validated_data.get('first_name', '').strip()
        last_name = validated_data.get('last_name', '').strip()
        
        if user_type == 'employer':
            validated_data['userDetails_emp'] = json.loads(details)
        
        if user_type == 'job_seeker':
            
            raw_details = self.initial_data['details']
            details = json.loads(raw_details)
            job_seeker_data = details.get('jobSeekerData', {})
            birthdate_str = job_seeker_data.get('birthdate')

            if birthdate_str:
                birthdate = date.fromisoformat(birthdate_str)
                today = date.today()

                age = today.year - birthdate.year
                if (today.month, today.day) < (birthdate.month, birthdate.day):
                    age -= 1

                # 👇 inject age into JSON
                job_seeker_data['age'] = age
                details['jobSeekerData'] = job_seeker_data

            validated_data['userDetails_job_seeker'] = details
        
        if user_type == 'supervisory':
            validated_data['userDetails_supervisory'] = json.loads(details)
        
        user = User(**validated_data)
        user.set_password(password) 
        user.role = user_type
        user.save()
        
        username = f"{last_name}{first_name}{user.id}".lower()
        user.username = username
        user.save(update_fields=['username'])
        return user
    
    def update(self, instance, validated_data):
        request = self.context.get("request")
        user = instance
        
        for field in [
            "avatar",
            "banner",
            "deleted_at",
        ]:
            if field in validated_data:
                setattr(user, field, validated_data[field])

        details = request.data.get("details", None)

        if details:
            details_data = json.loads(details) if isinstance(details, str) else details

            if user.role == "employer":
                user.userDetails_emp = details_data

            elif user.role == "job_seeker":
                user.userDetails_job_seeker = details_data
                
                resume_file = request.FILES.get("resume")  
                resume_info = details_data.get("resume_info", {})  

                if resume_file or resume_info:
                   
                    MyResume.objects.filter(user=user).delete()

                    MyResume.objects.create(
                        user=user,
                        resume=resume_file,
                        resume_info=resume_info
                    )


            elif user.role == "supervisory":
                user.userDetails_supervisory = details_data

        user.save()
        return user
    
    
    def get_fields(self):
        fields = super().get_fields()
        request = self.context.get('request')

        if request and request.method in ['PUT', 'PATCH']:
            fields['email'].required = False
            fields['password'].required = False
            # OPTIONAL: kung gusto, puwede rin optional ang avatar at banner
            fields['avatar'].required = False
            fields['banner'].required = False
        else:
            fields['email'].required = True

        return fields

    


        
class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'  
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # dito mo isinasama ang role sa token
        token['role'] = user.role
        token['email'] = user.email

        return token

    def validate(self, attrs):
        
        email = attrs.get("email")
        password = attrs.get("password")
       
        user = authenticate(username=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password")

        data = super().validate(attrs)
        data['user'] = {
            "id": self.user.id,
            "email": self.user.email,
            "username": self.user.username,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "is_email_verified": self.user.is_email_verified,
            "role": self.user.role
        }
        return data
    
    
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

class ResetPasswordSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(min_length=8, write_only=True)