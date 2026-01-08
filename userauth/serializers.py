
from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
import json

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email','password','deleted_at','first_name','last_name','userDetails_emp','userDetails_job_seeker','userDetails_supervisory']
        extra_kwargs = {
            'password': {'write_only': True, 'required': False},
            'username': {'read_only': True},
        }
        
        
    def create(self, validated_data):
        user_type = self.initial_data['user_type']
        details = self.initial_data['details']
        
        password = validated_data.pop('password', None) or 'defaultpassword123'
        first_name = validated_data.get('first_name', '').strip()
        last_name = validated_data.get('last_name', '').strip()
        
        
        if user_type == 'employer':
            validated_data['userDetails_emp'] = json.loads(details)
        
        if user_type == 'job_seeker':
            validated_data['userDetails_job_seeker'] = json.loads(details)
        
        if user_type == 'supervisory':
            validated_data['userDetails_supervisory'] = json.loads(details)
        

        user = User(**validated_data)
        user.set_password(password) 
        user.role = user_type
        user.save()
        
        username = f"{last_name}{first_name}{user.id}".lower()

        # Step 3: Update username and save again
        user.username = username
        user.save(update_fields=['username'])
        return user
        
        
class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'  

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
            "last_name": self.user.last_name
        }
        return data