from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPageNumberPagination(PageNumberPagination):
    """
    Custom page number pagination that allows clients to specify
    the number of items per page using the 'per_page' query parameter.

    Returns paginated response with additional metadata.
    """
    page_size_query_param = 'per_page'

    def get_paginated_response(self, data):
        """
        Construct a paginated response with metadata.

        Args:
            data: Serialized page data.

        Returns:
            Response: DRF Response containing page metadata and data.
        """
        return Response({
            'page': self.page.number,
            'per_page': self.page.paginator.per_page,
            'pages': self.page.paginator.num_pages,
            'has_next': self.page.has_next(),
            'data': data
        })
