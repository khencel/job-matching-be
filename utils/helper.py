from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status


class DynamicPageSizePagination(PageNumberPagination):
    
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


def paginate_queryset(request, queryset, serializer_class):
    paginator = DynamicPageSizePagination()
    page = paginator.paginate_queryset(queryset, request)

    serializer = serializer_class(page, many=True)
    return paginator.get_paginated_response(serializer.data)


