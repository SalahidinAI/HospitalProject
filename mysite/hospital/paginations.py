from rest_framework.pagination import PageNumberPagination


class TwoObject(PageNumberPagination):
    page_size = 2