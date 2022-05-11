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

class ListAPIUserWalletView(CustomListAPIView):

    permission_classes = [AllowAny]

    queryset = UserBitgoWalletAddress.objects.all()
    serializer_class = UserBitgoWalletAddressSerializer
    

class RetrieveWalletAPIView(CustomRetrieveAPIView):

    permission_classes = [AllowAny]

    queryset = UserBitgoWalletAddress.objects.all()
    serializer_class = UserBitgoWalletAddressSerializer
    lookup_field = 'id'

class CreateWalletAddressAPIView(CustomRetrieveAPIView):

    permission_classes = [AllowAny]

    queryset = UserBitgoWalletAddress.objects.all()
    serializer_class = UserBitgoWalletAddressSerializer

class UpdateWalletAddressAPIView(CustomUpdateAPIView):

    permission_classes = [AllowAny]

    queryset = UserBitgoWalletAddress.objects.all()
    serializer_class = UserBitgoWalletAddressSerializer
    lookup_field = 'id'

class DeleteWalletAddressAPIView(CustomDeleteAPIView):

    permission_classes = [AllowAny]

    queryset = UserBitgoWalletAddress.objects.all()
    serializer_class = UserBitgoWalletAddressSerializer
    lookup_field = 'id'


class CreateGetUserWalletView(CustomListCreateAPIView):

    permission_classes = [AllowAny]

    queryset = UserBitgoWalletAddress.objects.all()
    serializer_class = UserBitgoWalletAddressSerializer
        
class RetrieveUpdateDeleteItemWalletView(CustomRetrieveUpdateDeleteItem):

    permission_classes = [AllowAny]

    queryset = UserBitgoWalletAddress.objects.all()
    serializer_class = UserBitgoWalletAddressSerializer
    lookup_field = 'id'