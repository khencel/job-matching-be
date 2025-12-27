from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import JobPostSerializer
from .services.jobpost_service import create_jobpost
from .models import JobPost


class JobPostCreateView(APIView):
    def post(self, request):
        
        serializer = JobPostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        jobpost = create_jobpost(**serializer.validated_data)
        return Response(
            {
                "id": jobpost.id,
                "message": "Job post created successfully"
            }
            , status=status.HTTP_201_CREATED
        )
        
class JobPostListView(APIView):
    def get(self, request, user_id):
        jobposts = JobPost.objects.filter(user_id=user_id)
        serializer = JobPostSerializer(jobposts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)