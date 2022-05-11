from rest_framework import serializers
from api.models import UserBitgoWalletAddress


class UserBitgoWalletAddressSerializer(serializers.ModelSerializer):
    """
    This is for update ,Create
    """
    class Meta(object):
        model = UserBitgoWalletAddress
        fields = ('id', 'wallet_address', 'user')


