from rest_framework import serializers
from .models import MyResume



class MyResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyResume
        fields = '__all__'