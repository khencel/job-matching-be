from rest_framework import serializers
from .models import ApplicantDocument


class JobSeekerDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicantDocument
        fields = '__all__'