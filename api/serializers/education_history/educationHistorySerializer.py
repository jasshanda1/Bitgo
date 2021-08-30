from rest_framework import serializers
from api.models import EducationHistory
from django.core.exceptions import ValidationError
from day_beacon.settings import TIME12HRSFORMAT, DATEFORMAT


class CreateEducationHistorySerializer(serializers.ModelSerializer):
    """
    Create, update education hsitory of doctors.
    """
    class Meta(object):
        model = EducationHistory
        fields = ('id', 'user', 'degree_name', 'college_name', 'start', 'end', 'is_currenty')
    