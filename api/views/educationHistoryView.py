from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.schemas import AutoSchema
from rest_framework.compat import coreapi, coreschema
from api.services.education_history import EducationService

education_service = EducationService()

class CreateEducationView(APIView):
    def post(self, request, format=None):
        """
        create eduaction history
        """
        result = education_service.create_education_history(request, format=None)
        return Response(result, status=result["code"])