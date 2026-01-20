from rest_framework import serializers
from .models import JobApply

from post_a_job.models import JobPost
import post_a_job.serializers as JobPostSerializers
from userauth.models import User
from userauth.serializers import UserSerializer



class JobApplySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    job_post = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = JobApply
        fields = '__all__'
        
    def get_user(self, obj):
        user = obj.user
        serializer = UserSerializer(user)

      
        return {
            "userDetails": serializer.data['userDetails_job_seeker']['jobSeekerData'],
            "email": serializer.data['email'] 
        } 

    def get_job_post(self, obj):
        
        job_post = obj.job_post
        serializer = JobPostSerializers.JobPostSerializer(job_post)
        employer_id =serializer.data['user_id']
        
        user = User.objects.get(id=employer_id)
        userSerializer = UserSerializer(user)
        
        return {
            "jopPostDetails": serializer.data,   
            "employerDetails": userSerializer.data
        } 

       
        
        
        