from rest_framework import serializers
from .models import JobPost

class JobPostSerializer(serializers.ModelSerializer):
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
            "created_at"
        ]
        
    def validate_salary(self, value):
        if value < 0:
            raise serializers.ValidationError("Salary must be a positive integer.")
        return value