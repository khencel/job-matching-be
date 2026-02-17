from ..models import JobPost 

def create_jobpost(**validated_data):
    jobpost = JobPost.objects.create(**validated_data)
    return jobpost