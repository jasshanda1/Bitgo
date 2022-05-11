from pickle import NONE
from django import http

from os import access
from rest_framework import response
from api.models.userModel import User
from api.models.UploadMediaModel import UploadMedia
import re
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from django.template.loader import render_to_string
import json
import base64
import random
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from datetime import date, datetime, timedelta
import jwt
import requests
from api.serializers import user
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
from django.utils.deprecation import MiddlewareMixin
from api.utils.getUserByToken import get_user_by_token
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response


# class FilterUserIDMiddleware(MiddlewareMixin):
# 		# Check if user with this ID exists.
# 		def process_request(self, request):
# 			try:
# 				if request.META['HTTP_AUTHORIZATION']:
# 					user_details = get_user_by_token(request)
# 					user = user_details["user_id"]
# 					if User.objects.filter(id=user).exists():
# 						pass
# 					else:
# 						# #print("--------")
# 						# error_status_code = status.HTTP_403_FORBIDDEN
# 						# msg = "method=%s" % (request.method)
# 						# # msg = "method=%s path=%s status=%s request.body=%s response.body=%s" % (request.method,request.path,error_status_code,request._body_to_log,response.content)
# 						# #print("msg", msg)
# 						# return msg
# 						response = Response(
# 						{"detail": "This action is not authorized"},
# 						content_type="application/json",
# 						status=status.HTTP_401_UNAUTHORIZED,)
# 						response.accepted_renderer = JSONRenderer()
# 						response.accepted_media_type = "application/json"
# 						response.renderer_context = {}

# 						return response
# 			except Exception:
# 				pass


def simple_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = get_response(request)
        if response.status_code == 404:
            data = ({'data': None, 'status':status.HTTP_404_NOT_FOUND, 'message': 'object does not exist'})
            error_status_code = status.HTTP_404_NOT_FOUND
            response.status_code = error_status_code
            return Response(data=data, status=status.HTTP_404_NOT_FOUND)
        # Code to be executed for each request/response after
        # the view is called.
        # try:
        # 	user_details = get_user_by_token(request)
        # 	user = user_details["user_id"]
        # 	if User.objects.filter(id=user).exists():
        # 		pass
        # 	else:
        # 		error_status_code = status.HTTP_401_UNAUTHORIZED
        # 		response.status_code = error_status_code
        # except Exception:
        # 	pass
        print(response)
        return response

    return middleware