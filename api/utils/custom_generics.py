from __future__ import unicode_literals
from re import I
from httplib2 import Http
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveAPIView
from api.utils.custom_generic_views_functions import *

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

    def _get_queryset_return(self, klass):
        """
        Return a QuerySet or a Manager.
        Duck typing in action: any class with a `get()` method (for
        get_object_or_404) or a `filter()` method (for get_list_or_404) might do
        the job.
        """
        # If it is a model class or anything else with ._default_manager
        if hasattr(klass, '_default_manager'):
            return klass._default_manager.all()
        return klass

    def get_object_or_404_return(self, klass, *args, **kwargs):
        queryset = self._get_queryset_return(klass)
        if not hasattr(queryset, 'get'):
            klass__name = klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
            raise ValueError(
                "First argument to get_object_or_404() must be a Model, Manager, "
                "or QuerySet, not '%s'." % klass__name
            )
        try:
            return queryset.get(*args, **kwargs)
        except queryset.model.DoesNotExist:
            return 404

    def get_object(self):
        """
        Returns the object the view is displaying.

        You may want to override this if you need to provide non-standard
        queryset lookups.  Eg if objects are referenced using multiple
        keyword arguments in the url conf.
        """
        queryset = self.filter_queryset(self.get_queryset())

        # Perform the lookup filtering.
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field

        assert lookup_url_kwarg in self.kwargs, (
            'Expected view %s to be called with a URL keyword argument '
            'named "%s". Fix your URL conf, or set the `.lookup_field` '
            'attribute on the view correctly.' %
            (self.__class__.__name__, lookup_url_kwarg)
        )

        filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
        obj = self.get_object_or_404_return(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance == 404:
            data = ({'data': None, 'status':status.HTTP_404_NOT_FOUND, 'message': 'object does not exist.'})
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance)
        data = ({'data': serializer.data, 'status':status.HTTP_200_OK, 'message': 'OK'})
        return Response(data=data, status=status.HTTP_200_OK)
    
    """
    Destroy a model instance.
    """
    def destroy(self, request, *args, **kwargs): 
        instance = self.get_object()
        if instance == 404:
            data = ({'data': None, 'status':status.HTTP_404_NOT_FOUND, 'message': 'object does not exist.'})
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
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
        if instance == 404:
            data = ({'data': None, 'status':status.HTTP_404_NOT_FOUND, 'message': 'object does not exist.'})
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
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

class CustomListAPIView(CustomListCreateAPIView):
    pass

class CustomRetrieveAPIView(CustomRetrieveUpdateDeleteItem):
    pass

class CustomCreateAPIView(CustomListCreateAPIView):
    pass

class CustomUpdateAPIView(CustomRetrieveUpdateDeleteItem):
    pass

class CustomDeleteAPIView(CustomRetrieveUpdateDeleteItem):
    pass