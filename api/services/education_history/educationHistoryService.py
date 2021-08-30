from api.models import EducationHistory
from api.serializers.education_history import *
from api.utils import CustomPagination
from rest_framework import status
from api.utils.messages.commonMessages import *
from api.utils.messages.educationHistoryMessage import *

from .educationHistoryBaseService import EducationBaseService


class EducationService(EducationBaseService):
    """
    Create, Retrieve, Update or Delete a education history instance and Return all education history.
    """

    def __init__(self):
        pass

    def create_education_history(self, request, format=None):
        serializer = CreateEducationHistorySerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return({"data":serializer.data, "code":status.HTTP_201_CREATED, "message":EDUCATION_HISTORY_CREATED})
        #if not valid
        return({"data":serializer.errors, "code":status.HTTP_400_BAD_REQUEST, "message":BAD_REQUEST})