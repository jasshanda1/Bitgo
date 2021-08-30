from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.schemas import AutoSchema
from rest_framework.compat import coreapi, coreschema, uritemplate

from api.services.user import UserService

userService = UserService()

class SignupView(APIView):
    permission_classes = (AllowAny,)
    schema = AutoSchema(manual_fields=[
        coreapi.Field(
            "email",
            required=False,
            location="form",
            schema=coreschema.String()
        ),
        coreapi.Field(
            "phone_no",
            required=False,
            location="form",
            schema=coreschema.String()
        )    
    ])
    def post(self, request, format=None):
        """
        Create User/ Signup User
        """
        result = userService.sign_up(request, format=None)
        return Response(result, status=result["code"])

class VarifyOtpView(APIView):
    permission_classes = (AllowAny,)
    schema = AutoSchema(manual_fields=[
        coreapi.Field(
            "email",
            required=False,
            location="form",
            schema=coreschema.String()
        ),
        coreapi.Field(
            "phone_no",
            required=False,
            location="form",
            schema=coreschema.String()
        ),
        coreapi.Field(
            "otp",
            required=True,
            location="form",
            schema=coreschema.String()
        )
    ])
    def post(self, request, format=None):
        """
        verify otp
        """
        result = userService.verify_otp(request, format=None)
        return Response(result, status=result["code"])

class SendOtpForOldUser(APIView):
    permission_classes = (AllowAny,)
    schema = AutoSchema(manual_fields=[
        coreapi.Field(
            "phone_no",
            required=True,
            location="form",
            schema=coreschema.String()
        )
    ])
    def post(self, request, format=None):
        """
        Send OTP
        """
        result = userService.send_otp_for_old_user(request, format=None)
        return Response(result, status=result["code"])

class LoginView(APIView):
    permission_classes = (AllowAny,)
    schema = AutoSchema(manual_fields=[
        coreapi.Field(
            "email",
            required=True,
            location="form",
            schema=coreschema.String()
        ),
        coreapi.Field(
            "password",
            required=True,
            location="form",
            schema=coreschema.String()
        ),
        coreapi.Field(
            "device_id",
            required=False,
            location="form",
            schema=coreschema.String()
        ),
        coreapi.Field(
            "device-type",
            required=False,
            location="header",
            schema=coreschema.String()
        ),
        coreapi.Field(
            "app-version",
            required=False,
            location="header",
            schema=coreschema.String()
        )
    ])

    def post(self, request, format=None):
        """
        Login
        """
        role = [4,5,6,7]
        result = userService.login(request, role, format=None)
        return Response(result, status=result["code"])

class AdminLoginView(APIView):
    permission_classes = (AllowAny,)
    schema = AutoSchema(manual_fields=[
        coreapi.Field(
            "email",
            required=True,
            location="form",
            schema=coreschema.String()
        ),
        coreapi.Field(
            "password",
            required=True,
            location="form",
            schema=coreschema.String()
        ),
        coreapi.Field(
            "device_id",
            required=False,
            location="form",
            schema=coreschema.String()
        ),
        coreapi.Field(
            "device-type",
            required=False,
            location="header",
            schema=coreschema.String()
        ),
        coreapi.Field(
            "app-version",
            required=False,
            location="header",
            schema=coreschema.String()
        )
    ])

    def post(self, request, format=None):
        """
        Login
        """
        role = [1,2]
        result = userService.login(request, role, format=None)
        return Response(result, status=result["code"])

class ForgotPasswordView(APIView):
    """
    Forgot Password View
    """
    permission_classes = (AllowAny,)
    def put(self, request, format=None):
        result = userService.forgot_password(request, format=None)
        return Response(result, status=result["code"]) 
        
class LogoutView(APIView):
    """
    Logout
    """
    schema = AutoSchema(manual_fields=[

        coreapi.Field(
            "device-type",
            required=False,
            location="header",
            schema=coreschema.String()
        ),
        coreapi.Field(
            "device_id",
            required=False,
            location="form",
            schema=coreschema.String()
        ),
        coreapi.Field(
            "app-version",
            required=False,
            location="header",
            schema=coreschema.String()
        )

    ])

    def post(self, request, format=None):
        # simply delete the token to force a login
        result = userService.logout(request, format=None)
        return Response(result, status=result["code"])

class SetUserPasswordView(APIView):
    """
    set user password.
    """
    permission_classes = (AllowAny,)
    schema = AutoSchema(manual_fields=[
        coreapi.Field(
            "encoded_id",
            required=True,
            location="form",
            schema=coreschema.String()
        ),
        coreapi.Field(
            "password",
            required=True,
            location="form",
            schema=coreschema.String()
        )])
    def put(self, request, format=None):
        # simply delete the token to force a login
        result = userService.set_password(request, format=None)
        return Response(result, status=result["code"])

class AddUserDetialsView(APIView):
    """
    Add User Details
    """
    permission_classes = (AllowAny,)
    def put(self, request, format=None):
        result = userService.add_user_details(request, format=None)
        return Response(result, status=result["code"])


class CreateGetBranchView(APIView):
    """
    create branch view
    """
    permission_classes = (AllowAny,)
    def post(self, request, format=None):
        result = userService.create_branches(request, format=None)
        return Response(result, status=result["code"])

    def get(self, request, format=None):
        result = userService.get_all_branches(request, format=None)
        return Response(result, status=result["code"])


class CreateGetClassesView(APIView):
    """
    create classes view
    """
    permission_classes = (AllowAny,)
    def post(self, request, format=None):
        result = userService.create_classes(request, format=None)
        return Response(result, status=result["code"])

    def get(self, request, branch_id, format=None):
        result = userService.get_all_classes_by_branch_id(request, branch_id, format=None)
        return Response(result, status=result["code"])

class CreateGetSectionsView(APIView):
    """
    create sections view
    """
    permission_classes = (AllowAny,)
    def post(self, request, format=None):
        result = userService.create_sections(request, format=None)
        return Response(result, status=result["code"])

    def get(self, request, class_id, format=None):
        result = userService.get_all_sections_by_class_id(request, class_id, format=None)
        return Response(result, status=result["code"])


class ForgotVerifyOtpView(APIView):
    """
    Forgot Password verify otp View
    """
    permission_classes = (AllowAny,)
    def put(self, request, format=None):
        result = userService.forgot_verify_otp(request, format=None)
        return Response(result, status=result["code"])

class ChangePasswordView(APIView):
    """
    change Password after otp varification
    """
    permission_classes = (AllowAny,)
    def put(self, request, format=None):
        result = userService.change_password(request, format=None)
        return Response(result, status=result["code"])

class GetUserDetialsByTokenView(APIView):
    """
    Get User Details
    """
    def get(self, request, format=None):
        result = userService.get_user_details_by_token(request, format=None)
        return Response(result, status=result["code"])

class UpdatePasswordView(APIView):
    """
    Update Password View
    """
    def put(self, request, format=None):
        result = userService.updatePassword(request, format=None)
        return Response(result, status=result["code"])   

class UpdateUsersDetailsView(APIView):
    """
    Update User Details
    """
    def put(self, request, user_id, format=None):
        result = userService.update_profile_detials(request, user_id, format=None)
        return Response(result, status=result["code"])         

class GetAllTeacherClassDetails(APIView):
    """
    Update User Details
    """
    def get(self, request, format=None):
        result = userService.get_all_teahcer_class_details(request, format=None)
        return Response(result, status=result["code"]) 