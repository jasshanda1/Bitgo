from django.db.models import fields
from rest_framework import serializers
from api.models import (User)

from django.core.exceptions import ValidationError
from bitgo.settings import TIME12HRSFORMAT, DATEFORMAT
from api.serializers.uploadMedia import UploadMediaDetailsSerializer

class UserLoginDetailSerializer(serializers.ModelSerializer):
	"""
	Return the details of Login User.
	"""
	# dob = serializers.DateField(format=DATEFORMAT, input_formats=[DATEFORMAT])
	image = UploadMediaDetailsSerializer()
	class Meta(object):
		model = User
		fields = (
		'id', 'email', 'first_name', 'last_name', 'phone_no', 'is_active', 'is_deleted', "profile_status", "country_code", "image")
















	

