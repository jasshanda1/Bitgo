from __future__ import unicode_literals
from httplib2 import Http
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView

class CustomRetrieveAPIView(RetrieveAPIView):
    """
    Retrieve a model instance.
    """
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = ({'data': serializer.data, 'status':status.HTTP_200_OK, 'message': 'OK'})
        return Response(data=data, status=status.HTTP_200_OK)


class CustomListCreateAPIView(ListCreateAPIView):

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        data = ({'data': serializer.data, 'status':status.HTTP_200_OK, 'message': 'OK'})
        return Response(data=data, status=status.HTTP_200_OK)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            pass
        else:
            data = ({'data': None, 'status':status.HTTP_400_BAD_REQUEST, 'message': 'Something Went Wrong !'})
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = ({'data': serializer.data, 'status':status.HTTP_200_OK, 'message': 'OK'})
        return Response(data=data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class CustomRetrieveUpdateDeleteItem(RetrieveUpdateDestroyAPIView):
    """
    Retrieve a model instance.
    """

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        data = ({'data': serializer.data, 'status':status.HTTP_200_OK, 'message': 'OK'})
        return Response(data=data, status=status.HTTP_200_OK)
    
    """
    Destroy a model instance.
    """
    def destroy(self, request, *args, **kwargs): 
        instance = self.get_object()
        self.perform_destroy(instance)
        data = ({'data': None, 'status':status.HTTP_200_OK, 'message': 'OK'})
        return Response(data=data, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()
    
    """
    Update a model instance.
    """
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        data = ({'data': serializer.data, 'status':status.HTTP_200_OK, 'message': 'OK'})
        return Response(data=data, status=status.HTTP_200_OK)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)