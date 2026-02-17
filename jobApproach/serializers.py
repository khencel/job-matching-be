from rest_framework import serializers
from .models import JobApproach

class JobSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApproach
        fields = [
            "data",
        ]