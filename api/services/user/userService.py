from rest_framework import status
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from django.template.loader import render_to_string
# from twilio.rest import Client
import json
import base64
import random
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate, login
from django.core.mail import EmailMultiAlternatives
import pytz
from datetime import datetime, timedelta
import jwt
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

from django.core.files.base import ContentFile

from .userBaseService import UserBaseService
from api.utils.messages.userMessages import *
from api.utils.messages.commonMessages import *
from api.models import User, UserSession, Role, UserClassDetails
from api.utils.getUserByToken import get_user_by_token
from api.serializers.user import *
from day_beacon import settings

class UserService(UserBaseService):
	"""
	Allow any user (authenticated or not) to access this url 
	"""

	def __init__(self):
		pass

	def login(self, request, role, format=None):

		validated_data = self.validate_auth_data(request)

		if "email" in request.data:
			username = request.data['email'].lower()
			country_code = None
		else:
			username = request.data['phone_no']
			country_code = request.data['country_code']

		password = request.data['password']

	
		user = self.user_authenticate(username, password, role, country_code)
		
		if user is not None:
			if user.otp_varification is True:

				login(request, user)

				serializer = UserLoginDetailSerializer(user)

				payload = jwt_payload_handler(user)
				token = jwt.encode(payload, settings.SECRET_KEY)

				user_details = serializer.data
				if user.profile_status == 4:
					user_details['token'] = token
					# User.objects.filter(pk=user.pk).update(auth_token=token)

					user_session = self.create_update_user_session(user, token, request)
	
				return ({"data": user_details,"code": status.HTTP_200_OK,"message": "LOGIN_SUCCESSFULLY"})
			return ({"data":None, "code":status.HTTP_400_BAD_REQUEST, "message":"your account is not varified. please firstly verify to your account please press below button send otp to verify your account."})
		return ({"data": None,"code": status.HTTP_400_BAD_REQUEST, "message": "INVALID_CREDENTIALS"})

	def user_authenticate(self, user_name, password, role, country_code):
		print(user_name)
		try:
			user = User.objects.get(email=user_name, role__in=role)
			if user.check_password(password):
				return user # return user on valid credentials
		except User.DoesNotExist:
			try:
				user = User.objects.get(phone_no=user_name, country_code=country_code, role__in=role)
				print(user)
				if user.check_password(password):
					return user # return user on valid credentials
			except User.DoesNotExist:
				return None

	def validate_auth_data(self, request):
		error = {}
		if not request.data.get('email'):
			error.update({'email' : "FIELD_REQUIRED" })

		if not request.data.get('password'):
			error.update({'password' : "FIELD_REQUIRED" })

		if request.headers.get('device-type')=='android'or request.headers.get('device-type')=='ios':
			if not request.data.get('device_id'):
				error.update({'device_id': "FIELD_REQUIRED"})

		if error:
			raise ValidationError(error)
	
	def create_update_user_session(self, user, token, request):
		"""
		Create User Session
		"""
		print(request.headers.get('device-type'))
		print(request.data.get('device_id'))

		user_session = self.get_user_session_object(user.pk, request.headers.get('device-type'), request.data.get('device_id'))

		if user_session is None:
			UserSession.objects.create(
				user = user,
				token = token,
				device_id = request.data.get('device_id'),
				device_type = request.headers.get('device-type'),
				app_version = request.headers.get('app-version')
			)

		else:
			user_session.token = token
			user_session.app_version = request.headers.get('app-version')
			user_session.save()

		return user_session

	
	def get_user_session_object(self, user_id, device_type, device_id=None):
		try:
			if device_id:
				try:
					return UserSession.objects.get(user=user_id, device_type=device_type, device_id=device_id)
				except UserSession.DoesNotExist:
					return None

			return UserSession.objects.get(user=user_id, device_type=device_type, device_id=device_id)

		except UserSession.DoesNotExist:
			return None

	def generate_encoded_id(self, obj):
		encoded_id = base64.b64encode(str(random.randint (10000000, 99990000)).encode("ascii")).decode("ascii")
		obj.encoded_id = encoded_id
		obj.save()
		return "success"

	def send_otp_on_mail(self, email):
		print(email)
		try:
			member_time_zone = "UTC"
			tz = pytz.timezone(member_time_zone)

			current_time = datetime.now(tz)
			try:
				user = User.objects.get(email=email.lower())
			except User.DoesNotExist:
				raise Exception ({
					'email': EMAIL_NOT_EXIST
				})

			otp = random.randint (1000, 9999)
			user.otp = otp
			user.otp_varification = False
			user.otp_send_time = current_time
			user.save ()
			context = {"otp":otp}
			body_msg = render_to_string ('api/email/email-confirmation.html', context)
			msg = EmailMultiAlternatives ("Email Varification<Don't Reply>", body_msg, "sagarseth@apptunix.com", [email])
			msg.content_subtype = "html"
			msg.send()


			return "Success"
		except Exception as e:
			print(e)
			pass

	def send_mobile_otp(self, user):
		try:
			tz = pytz.timezone ('Asia/Kolkata')
			current_time = datetime.now (tz)

			# user = self.get_object_by_email (email)
			otp = random.randint (100000, 999999)
			body_msg = 'Your OTP is {} . OTP is valid for 1 hour or 1 successfull attempt.'.format (
				otp)
			account_sid = "AC3c90cc753940be88466d44fa3066cf23"
			auth_token = "fdc70d87eac59a4074bc9cf54d0cc336"
			# client = Client(account_sid, auth_token)
			# message = client.messages.create(
			#         to="+91{}".format("8146664616"), 
			#         from_="+18152013322",
			#         body=body_msg)

			user.otp = 1102
			user.otp_send_time = current_time
			user.save ()

			
		except Exception as e:
			raise ValidationError(e)

	def sign_up(self, request, format=None):
		role = Role.objects.get(id=3)
		if "email" in request.data:
			try:
				user = User.objects.get(email=request.data["email"].lower())
				self.generate_encoded_id(user)
				if int(user.profile_status) >= 3:
					return({"data":None, "code":status.HTTP_400_BAD_REQUEST, "message":EMAIL_ALREADY_EXIST})
				else:
					self.send_otp_on_mail(request.data["email"])
					return({"data":None, "code":status.HTTP_200_OK, "message":OTP_SENT})
			except User.DoesNotExist:
				user = User.objects.create(email=request.data["email"].lower(), user_name = request.data["email"], profile_status=1)
				self.generate_encoded_id(user)
				self.send_otp_on_mail(request.data["email"])
				return({"data":None, "code":status.HTTP_200_OK, "message":OTP_SENT})
		else:
			try:
				user = User.objects.get(country_code = request.data["country_code"],phone_no=request.data["phone_no"])  
				self.generate_encoded_id(user)
				if int(user.profile_status) <= 3:
					return({"data":None, "code":status.HTTP_400_BAD_REQUEST, "message":EMAIL_ALREADY_EXIST})
				else:
					self.send_mobile_otp(user)
					return({"data":None, "code":status.HTTP_200_OK, "message":OTP_SENT})
			except User.DoesNotExist:
				user = User.objects.create(country_code = request.data["country_code"], phone_no=request.data["phone_no"], user_name=request.data["phone_no"], profile_status=1)
				self.generate_encoded_id(user)
				self.send_mobile_otp(user)
				return({"data":None, "code":status.HTTP_200_OK, "message":OTP_SENT})
	
	def validate_signup_data(self, data):
		try:
			user = User.objects.get(phone_no=data.get('phone_no'))
			raise ValidationError({"phone_no": "you are already registered with this phone no. if you not remeber your password then click on Forgot Passowrd!!"})
		except User.DoesNotExist:
			return None

	# def send_otp(self, user):
	# 	try:
	# 		tz = pytz.timezone ('Asia/Kolkata')
	# 		current_time = datetime.now (tz)

	# 		# user = self.get_object_by_email (email)
	# 		otp = random.randint (100000, 999999)
	# 		body_msg = 'Your OTP is {} . OTP is valid for 1 hour or 1 successfull attempt.'.format (
	# 			otp)
	# 		account_sid = "AC3c90cc753940be88466d44fa3066cf23"
	# 		auth_token = "fdc70d87eac59a4074bc9cf54d0cc336"
	# 		# client = Client(account_sid, auth_token)
	# 		# message = client.messages.create(
	# 		#         to="+91{}".format("8146664616"), 
	# 		#         from_="+18152013322",
	# 		#         body=body_msg)

	# 		user.otp = 1102
	# 		user.otp_send_time = current_time
	# 		user.save ()

			
	# 	except Exception as e:
	# 		raise ValidationError(e)
	
	def send_otp_for_old_user(self, request, format=None):
		try:
			tz = pytz.timezone ('Asia/Kolkata')
			current_time = datetime.now (tz)
			if "email" in request.data and len(request.data["email"]) != 0:
				try:
					user = User.objects.get(email=request.data["email"])
					self.send_otp_on_mail(user.email)
					return ({"data":None, "code":status.HTTP_200_OK, "message":OTP_SENT})
				except User.DoesNotExist:
					return ({"data":None, "code":status.HTTP_400_BAD_REQUEST, "message":RECORD_NOT_FOUND})
			else:
				try:
					user = User.objects.get(phone_no=request.data["phone_no"], country_code = request.data["country_code"])
				except User.DoesNotExist:
					return ({"data":None, "code":status.HTTP_400_BAD_REQUEST, "message":RECORD_NOT_FOUND})

			otp = random.randint (1000, 9999)
			body_msg = 'Your OTP is {} . OTP is valid for 1 hour or 1 successfull attempt.'.format (
				otp)
			account_sid = "AC3c90cc753940be88466d44fa3066cf23"
			auth_token = "fdc70d87eac59a4074bc9cf54d0cc336"
			# client = Client(account_sid, auth_token)
			# message = client.messages.create(
			#         to="+91{}".format("8146664616"), 
			#         from_="+18152013322",
			#         body=body_msg)

			user.otp = 1289
			user.otp_send_time = current_time
			user.save ()

			
		except Exception as e:
			raise ValidationError(e)

		return ({"data":None, "code":status.HTTP_200_OK, "message":"OTP Sent Successfully"})

	def verify_otp(self, request, format=None):
		# self.validate_otp_data (request.data)
		tz = pytz.timezone ('Asia/Kolkata')
		current_time = datetime.now (tz)
		now_date = current_time.strftime ('%m/%d/%y')
		now_time = current_time.strftime ('%H:%M')

		otp = request.data['otp']
		user = None
		if "email" in request.data and len(request.data["email"]) != 0:
			try:
				user = User.objects.get(email=request.data["email"])
			except User.DoesNotExist:
				user = None
		else:
			try:
				user = User.objects.get(phone_no=request.data["phone_no"], country_code = request.data["country_code"])
			except User.DoesNotExist:
				user = None

		if user:
			if user.otp_varification is False:
				if int(user.otp) == int(otp):
					otp_send_time = user.otp_send_time
					otp_send_time = otp_send_time.astimezone (tz) + timedelta (hours=1)

					otp_date = datetime.strftime (otp_send_time, '%m/%d/%y')
					otp_time = datetime.strftime (otp_send_time, '%H:%M')

					if now_date == otp_date and now_time <= otp_time:
						user.otp_varification = True
						user.profile_status = 2
						user.save()
						return {"data": {"user":user.encoded_id}, "code": status.HTTP_200_OK, "message": OTP_VERIFID}
					else:
						return {"data": None, "code": status.HTTP_400_BAD_REQUEST, "message": OTP_EXPIRED}
				else:
					return ({"data":None, "code":status.HTTP_400_BAD_REQUEST, "message":WRONG_OTP})
			else:
				return ({"data":None, "code":status.HTTP_400_BAD_REQUEST, "message":NUMBER_ALREADY_VARIFIED})        
			
		else:
			return {"data": None, "code": status.HTTP_400_BAD_REQUEST, "message": DETAILS_INCORRECT}

	def logout(self, request, format=None):

		validated_data = self.validate_logout_data(request)
		try:
			jwt_token_str = request.META['HTTP_AUTHORIZATION']
			jwt_token = jwt_token_str.replace('Bearer', '')
			user_detail = jwt.decode(jwt_token, None, None)
			user = User.objects.get(pk=user_detail['user_id'])

			user_session_instance = self.get_user_session_object(user.pk, request.headers.get('device-type'), request.data.get('device_id'))

			if user_session_instance:
				user_session = self.create_update_user_session(user, None, request)
				return ({"data": None, "code": status.HTTP_200_OK, "message": "LOGOUT_SUCCESSFULLY"})
			else:
				return ({"data":None, "code":status.HTTP_400_BAD_REQUEST, "message":"RECORD_NOT_FOUND"})

		except User.DoesNotExist:
			return ({"data": None, "code": status.HTTP_400_BAD_REQUEST, "message": "RECORD_NOT_FOUND"})

	def set_password(self, request, format=None):
		try: 
			user = User.objects.get(encoded_id = request.data["encoded_id"])
			user.set_password(request.data["password"])
			user.profile_status = 3
			user.save()
			self.generate_encoded_id(user)
			return({"data":{"user":user.encoded_id}, "code":status.HTTP_200_OK, "message":"Password set successfully !"})
		except User.DoesNotExist:
			return({"data":None, "code":status.HTTP_400_BAD_REQUEST, "message":"You Entered wrong encoded id"})

	
	def add_user_details(self, request, format=None):
		"""
		Add user details
		"""
		try: 
			user = User.objects.get(encoded_id = request.data["encoded_id"])
			serializer = UserCreateUpdateSerializer(user, data=request.data)
			if serializer.is_valid():
				serializer.save()
				return({"data":None, "code":status.HTTP_200_OK, "message":"User Details Added successfully"})
			return({"data":serializer.errors, "code":status.HTTP_400_BAD_REQUEST, "message":OK})
		except User.DoesNotExist:
			return({"data":None, "code":status.HTTP_400_BAD_REQUEST, "message":"You Entered wrong encoded id"})

	def create_branches(self, request, format=None):
		"""
		create branches
		"""
		serializer = CreateBranchesSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return({"data":None, "code":status.HTTP_201_CREATED, "message":"Branch Created SuccessFully !"})
		#if not valid
		return({"data":serializer.errors, "code":status.HTTP_400_BAD_REQUEST, "message":BAD_REQUEST})
	
	def create_classes(self, request, format=None):
		"""
		create Classes
		"""
		serializer = CreateClassesSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return({"data":None, "code":status.HTTP_201_CREATED, "message":"Class Created SuccessFully !"})
		#if not valid
		return({"data":serializer.errors, "code":status.HTTP_400_BAD_REQUEST, "message":BAD_REQUEST})
	
	def create_sections(self, request, format=None):
		"""
		create Sections
		"""
		serializer = CreateClassSectionSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return({"data":None, "code":status.HTTP_201_CREATED, "message":"Class Section Created SuccessFully !"})
		#if not valid
		return({"data":serializer.errors, "code":status.HTTP_400_BAD_REQUEST, "message":BAD_REQUEST})


	def get_all_branches(self, request, format=None):
		"""
		get all branches
		"""
		branch_objs = Branch.objects.all()
		serializer = GetBranchesSerializer(branch_objs, many=True)
		return({"data":serializer.data, "code":status.HTTP_200_OK, "message":OK})

		
	
	def get_all_classes_by_branch_id(self, request, branch_id, format=None):
		"""
		get all Classes
		"""
		class_objs = Classes.objects.filter(branch = branch_id)
		serializer = GetClassesSerializer(class_objs, many=True)
		return({"data":serializer.data, "code":status.HTTP_200_OK, "message":OK})
	
	def get_all_sections_by_class_id(self, request, class_id, format=None):
		"""
		get all Sections
		"""
		sections_objs = ClassSection.objects.filter(section_class = class_id)
		serializer = GetClassSectionSerializer(sections_objs, many=True)
		return({"data":serializer.data, "code":status.HTTP_200_OK, "message":OK})
	
	def forgot_password(self, request, format=None):
		"""
		This method is for Forgot password.
		"""
		if "email" in request.data:
			
			try:
				tz = pytz.timezone ('Asia/Kolkata')
				current_time = datetime.now (tz)
				user = User.objects.get(email=request.data.get("email"))
				otp = random.randint (1000, 9999)
				user.otp = otp
				user.otp_varification = False
				user.otp_send_time = current_time
				user.save ()
				context = {"otp":otp}
				body_msg = render_to_string ('api/email/forgot-password-email.html', context)
				msg = EmailMultiAlternatives ("Email Varification<Don't Reply>", body_msg, "sagarseth@apptunix.com", [user.email])
				msg.content_subtype = "html"  
				msg.send()
				return({"data":None, "code":status.HTTP_200_OK, "message": OTP_SENT})
			except Exception as e:
				return({"data":None, "code":status.HTTP_400_BAD_REQUEST, "message": RECORD_NOT_FOUND})
		else:
			try:
				user = User.objects.get(country_code=request.data.get("country_code"),phone_no=request.data.get("phone_no"))
				tz = pytz.timezone ('Asia/Kolkata')
				current_time = datetime.now (tz)
				otp = random.randint (1000, 9999)
				body_msg = 'Your OTP is {} . OTP is valid for 1 hour or 1 successfull attempt.'.format (
				otp)
				account_sid = "AC3c90cc753940be88466d44fa3066cf23"
				auth_token = "fdc70d87eac59a4074bc9cf54d0cc336"
				user.otp = 1289
				user.otp_send_time = current_time
				user.save ()
				return({"data":None, "code":status.HTTP_200_OK, "message": OTP_SENT})
			except User.DoesNotExist:
				return({"data":None, "code":status.HTTP_400_BAD_REQUEST, "message": RECORD_NOT_FOUND})

	def forgot_verify_otp(self, request, format=None):
		tz = pytz.timezone ('Asia/Kolkata')
		current_time = datetime.now (tz)
		now_date = current_time.strftime ('%m/%d/%y')
		now_time = current_time.strftime ('%H:%M')

		otp = request.data['otp']
		user = None
		if "email" in request.data and len(request.data["email"]) != 0:
			try:
				user = User.objects.get(email=request.data["email"])
			except User.DoesNotExist:
				user = None
		else:
			try:
				user = User.objects.get(phone_no=request.data["phone_no"], country_code = request.data["country_code"])
			except User.DoesNotExist:
				user = None

		if user:
			if int(user.otp) == int(otp):
				otp_send_time = user.otp_send_time
				otp_send_time = otp_send_time.astimezone (tz) + timedelta (minutes=10)

				otp_date = datetime.strftime (otp_send_time, '%m/%d/%y')
				otp_time = datetime.strftime (otp_send_time, '%H:%M')

				if now_date == otp_date and now_time <= otp_time:
					user.otp_varification = True
					user.save()
					return {"data": None, "code": status.HTTP_200_OK, "message": OTP_VERIFID}
				else:
					return {"data": None, "code": status.HTTP_400_BAD_REQUEST, "message": OTP_EXPIRED}
			else:
				return ({"data":None, "code":status.HTTP_400_BAD_REQUEST, "message":WRONG_OTP})
		else:
			return {"data": None, "code": status.HTTP_400_BAD_REQUEST, "message": DETAILS_INCORRECT}


	def change_password(self, request, format=None):
		if "email" in request.data and len(request.data["email"]) != 0:
			try:
				user = User.objects.get(email=request.data["email"])
			except User.DoesNotExist:
				user = None
		else:
			try:
				user = User.objects.get(phone_no=request.data["phone_no"], country_code = request.data["country_code"])
			except User.DoesNotExist:
				user = None
		
		if user:
			user.set_password(request.data["password"])
			user.save()
			return({"data":None, "code":status.HTTP_200_OK, "message":"Password updated successfully !"})
		else:
			return({"data":None, "code":status.HTTP_204_NO_CONTENT, "message":RECORD_NOT_FOUND})
	
	def get_user_details_by_token(self, request, format=None):
		try:
			user_details = get_user_by_token(request)
			details_obj =  User.objects.get(pk=user_details["user_id"])
			serializer= UserDetialsSerializer(details_obj)
			return({"data":serializer.data, "code":status.HTTP_200_OK, "message":OK})
		except User.DoesNotExist:
			return({"data":None, "code":status.HTTP_400_BAD_REQUEST, "message":RECORD_NOT_FOUND})
	
	def updatePassword(self, request, format=None):
		user_details = get_user_by_token(request)
		try:
			user = User.objects.get(id=user_details["user_id"])
		except User.DoesNotExist:
			user = None
		if user is not None:
			if user is not None:
				current_password = request.data.get("current_password")
			if user.check_password(current_password):
				user.set_password(request.data.get("new_password"))
				user.save()
				return({"data":None, "code":status.HTTP_200_OK, "message": PASSWORD_CHANGE_SUCCESSFULLY})
			else:
				return({"data":None, "code":status.HTTP_400_BAD_REQUEST, "message": INVALID_WRONG_PASSWORD})

		else:
			return({"data":None, "code":status.HTTP_400_BAD_REQUEST, "message": RECORD_NOT_FOUND})

	def update_profile_detials(self, request, user_id , format=None):
		"""
		Updates detail
		"""
		data = request.data
		user_details = get_user_by_token(request)
		user = User.objects.get(id=user_id)
		serializer = UserUpdateDetialsSerializer(user, data=data)
		if serializer.is_valid ():
			serializer.save ()
			return ({"data": serializer.data, "code": status.HTTP_200_OK,"message":USER_DETAIL_UPDATED})
		else:
			return ({"data": serializer.errors, "code": status.HTTP_400_BAD_REQUEST,"message":BAD_REQUEST})

	def get_all_teahcer_class_details(self, request, format=None):
		"""
		get all teacher classes details.
		"""
		user_id = get_user_by_token(request)["user_id"]
		user_class = UserClassDetails.objects.filter(user=user_id)
		serializer = GetUserClassDetailsSerializer(user_class, many=True)
		return({"data":serializer.data, "code":status.HTTP_200_OK, "message":OK})

