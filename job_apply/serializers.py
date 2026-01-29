from rest_framework import serializers
from .models import JobApply

from post_a_job.models import JobPost
import post_a_job.serializers as JobPostSerializers
from userauth.models import User
from userauth.serializers import UserSerializer
from my_resume.models import MyResume
from my_resume.serializers import MyResumeSerializer




class JobApplySerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)
    job_post = serializers.SerializerMethodField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True, source='user'
    )
    job_post_id = serializers.PrimaryKeyRelatedField(
        queryset=JobPost.objects.all(), write_only=True, source='job_post'
    )
    
    class Meta:
        model = JobApply
        fields = '__all__'
        
    def get_user(self, obj):
        user = obj.user
        serializer = UserSerializer(user)

        job_seeker_data = None
        try:
            job_seeker_data = serializer.data['userDetails_job_seeker']['jobSeekerData']
            
            myresume = MyResume.objects.get(user=user)
            resume_serializer = MyResumeSerializer(myresume)
           
            
        except (TypeError, KeyError):
            job_seeker_data = serializer.data.get('userDetails_job_seeker')

        return {
            "userDetails": job_seeker_data,
            "email": serializer.data.get('email'), 
            "avatar": serializer.data.get('avatar'),
            "resume": resume_serializer.data if myresume else None
        } 

    def get_job_post(self, obj):
        job_post = obj.job_post
        serializer = JobPostSerializers.JobPostSerializer(job_post)
        employer_id = serializer.data.get('user_id')

        employer_data = None
        if employer_id:
            try:
                user = User.objects.get(id=employer_id)
                userSerializer = UserSerializer(user)
                employer_data = userSerializer.data
            except User.DoesNotExist:
                employer_data = None
        
        return {
            "jobPostDetails": serializer.data,   
            "employerDetails": employer_data
        } 

       
        
        
        