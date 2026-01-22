from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import JobApply
from .serializers import JobApplySerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError



class DynamicPageSizePagination(PageNumberPagination):
    
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    
class JobApplyView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        page_size = request.query_params.get('page_size', 10)
        
        try:
            page_size = int(page_size)
        
            if page_size > 100:
                page_size = 100
            if page_size < 1:
                page_size = 10
        except ValueError:
            page_size = 10
            
        try:
            job_apply = JobApply.objects.all()
            
            
            paginator = DynamicPageSizePagination()
            paginator.page_size = page_size  


            paginated_job_apply = paginator.paginate_queryset(job_apply, request)

            serializer = JobApplySerializer(paginated_job_apply, many=True)
            
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    def post(self, request):
        try:
            # allow clients to POST with keys `user` and `job_post` (ids)
            data = request.data
            try:
                payload = data.copy()
            except Exception:
                payload = dict(data)

            # default to authenticated user if not provided
            if 'user_id' not in payload and 'user' not in payload:
                payload['user_id'] = request.user.id

            # map legacy keys to the write-only fields
            if 'user' in payload and 'user_id' not in payload:
                payload['user_id'] = payload.get('user')
            if 'job_post' in payload and 'job_post_id' not in payload:
                payload['job_post_id'] = payload.get('job_post')

            serializer = JobApplySerializer(data=payload)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
