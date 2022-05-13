from cgitb import lookup
import re
import requests
from bitgo import settings
from traceback import print_tb
from docutils import DataError
# from typing_extensions import Self
from rest_framework.generics import ListCreateAPIView
from api.models.UserBitgoWalletAddress import *
from api.serializers.userBitgoWalletAddress.UserBitgoWalletAddress import UserBitgoWalletAddressSerializer
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
import json
from api.utils.custom_generics import *
from rest_framework.generics import RetrieveAPIView
from rest_framework.generics import ListAPIView
from api.serializers.user import UserLoginDetailSerializer

class WebhookView(CustomRetrieveAPIView):

	permission_classes = [AllowAny]

	queryset = User.objects.none()
	serializer_class = UserLoginDetailSerializer()
	lookup_field = "id"
	def get_queryset(self):
		print("------------------------")
		print("hkdvfhv")
		return User.objects.get(id = 1)