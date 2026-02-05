from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import JobPostSerializer
from .services.jobpost_service import create_jobpost
from .models import JobPost
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404


class JobPostCreateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request):
        
        serializer = JobPostSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        jobpost = serializer.save()

        return Response(
            {
                "id": jobpost.id,
                "message": "Job post created successfully"
            },
            status=status.HTTP_201_CREATED
        )
        
class DynamicPageSizePagination(PageNumberPagination):
    
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
        
class JobPostListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    serializer_class = JobPostSerializer
    pagination_class = DynamicPageSizePagination
    
    def get(self, request, user_id):
        page_size = request.query_params.get('page_size', 10)
        
        try:
            page_size = int(page_size)
        
            if page_size > 100:
                page_size = 100
            if page_size < 1:
                page_size = 10
        except ValueError:
            page_size = 10
        
        
        jobposts = JobPost.objects.filter(user_id=user_id,deleted=False).order_by('-created_at')
        
       
        paginator = DynamicPageSizePagination()
        paginator.page_size = page_size  
        
       
        paginated_jobposts = paginator.paginate_queryset(jobposts, request)
        
      
        serializer = JobPostSerializer(paginated_jobposts, many=True)
        
    
        return paginator.get_paginated_response(serializer.data)
    
class DeleteJobPostView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, pk):
        try:
            jobpost = JobPost.objects.get(pk=pk)
            jobpost.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except JobPost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class JobPostListAllView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    
    def get(self, request):
        jobposts = JobPost.objects.filter(is_active=True)
        serializer = JobPostSerializer(jobposts, many=True)
        return Response(serializer.data)
    
class JobPostDetailsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        try:
            jobpost = JobPost.objects.get(pk=pk)
            serializer = JobPostSerializer(jobpost)
            return Response(serializer.data)
        except JobPost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class JobPostUpdate(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        try:
            jobpost = JobPost.objects.get(pk=pk)
        except JobPost.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = JobPostSerializer(jobpost, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data)
    
class JobPostChangeStatus(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        job_post = get_object_or_404(JobPost, id=pk)
        job_post.is_active = not job_post.is_active
        job_post.save()
        return Response({
            "value":True,
            "message":"status has been change"
        })
        