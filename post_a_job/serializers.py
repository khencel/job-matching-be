from rest_framework import serializers
from .models import JobPost
from userauth.models import User
from userauth.serializers import UserSerializer

class JobPostSerializer(serializers.ModelSerializer):
    employer = serializers.SerializerMethodField()
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = JobPost
        fields = [
            "id",
            "user_id",
            "title",
            "salary",
            "type_of_emp",
            "category",
            "skill",
            "job_desc",
            "responsibility",
            "who_you_are",
            "nice_to_have",
            "benefits",
            "created_at",
            "employer"
        ]
        
    def get_employer(self, obj):
        user_id = obj.user_id
        user = User.objects.filter(id=user_id).values("avatar","userDetails_emp")
        
        return user
        
    def validate_salary(self, value):
        if value < 0:
            raise serializers.ValidationError("Salary must be a positive integer.")
        return value
    
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user_id'] = user.id
        return JobPost.objects.create(**validated_data)