from django.db.models import fields
from rest_framework import serializers
from api.models import (User, Branch, Classes, ClassSection, UserClassDetails, UserSectionDetails)

from django.core.exceptions import ValidationError
from day_beacon.settings import TIME12HRSFORMAT, DATEFORMAT
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

class CreateUpdateUserSectionDetailsSerializer(serializers.ModelSerializer):
	"""
	create/update user class Details
	"""
	id = serializers.IntegerField(required=False)
	class Meta:
		model = UserSectionDetails
		fields = ("id", "section")

class CreateUpdateUserClassDetailsSerializer(serializers.ModelSerializer):
	"""
	create/update user class Details
	"""
	id = serializers.IntegerField(required=False)
	user_sections = CreateUpdateUserSectionDetailsSerializer(many=True)
	class Meta:
		model = UserClassDetails
		fields = ("id", "classes", "branch", "user_sections")
class UserCreateUpdateSerializer(serializers.ModelSerializer):
	"""
	create/update user .
	"""
	id = serializers.IntegerField(required=False)
	user_classes = CreateUpdateUserClassDetailsSerializer(many=True)
	class Meta:
		model = User
		fields = ('id', 'first_name', 'wristband_id', 'phone_no', 'email', 'country_code', 'role', 'gender', 'address', 'longitude', 'latitude', 'image', "user_classes")       

	def update(self, instance, validated_data):
		instance.first_name = validated_data['first_name']
		instance.wristband_id = validated_data['wristband_id']
		instance.email = validated_data['email']
		instance.country_code = validated_data['country_code']
		instance.phone_no = validated_data['phone_no']
		instance.address = validated_data['address']
		if 'longitude' in validated_data:
			instance.longitude = validated_data['longitude']
		if 'latitude' in validated_data:
			instance.latitude = validated_data['latitude']
		instance.gender = validated_data['gender']
		instance.role = validated_data['role']
		instance.image = validated_data['image']
		instance.encoded_id = None
		instance.is_active = True
		instance.profile_status = 4
		instance.save()

		for classes in validated_data["user_classes"]:
			sections = classes.pop("user_sections")
			class_details_obj = UserClassDetails.objects.create(user=instance, **classes)
			for section_data in sections:
				UserSectionDetails.objects.create(user_class=class_details_obj, **section_data)

		return instance

class CreateBranchesSerializer(serializers.ModelSerializer):
	"""
	create branches
	"""
	class Meta:
		model = Branch
		fields = ("id", "name")

class CreateClassesSerializer(serializers.ModelSerializer):
	"""
	create classes
	"""
	class Meta:
		model = Classes
		fields = ("id", "name", "branch")


class CreateClassSectionSerializer(serializers.ModelSerializer):
	"""
	create class sections
	"""
	class Meta:
		model = ClassSection
		fields = ("id", "name", "section_class")



class GetBranchesSerializer(serializers.ModelSerializer):
	"""
	Get branches
	"""
	class Meta:
		model = Branch
		fields = ("id", "name")

class GetClassesSerializer(serializers.ModelSerializer):
	"""
	Get classes
	"""
	branch = GetBranchesSerializer()
	class Meta:
		model = Classes
		fields = ("id", "name", "branch")


class GetClassSectionSerializer(serializers.ModelSerializer):
	"""
	Get class sections
	"""
	section_class = GetClassesSerializer()
	class Meta:
		model = ClassSection
		fields = ("id", "name", "section_class")


class GetUserSectionDetailsSerializer(serializers.ModelSerializer):
	"""
	Get user class Details
	"""
	section = GetClassSectionSerializer()
	class Meta:
		model = UserSectionDetails
		fields = ("id", "section")

class GetUserClassDetailsSerializer(serializers.ModelSerializer):
	"""
	Get user class Details
	"""
	user_sections = GetUserSectionDetailsSerializer(many=True)
	classes = GetClassesSerializer()
	branch = GetBranchesSerializer()
	class Meta:
		model = UserClassDetails
		fields = ("id", "classes", "branch", "user_sections")

class UserDetialsSerializer(serializers.ModelSerializer):
	"""
	Get user Detials.
	"""
	user_classes = GetUserClassDetailsSerializer(many=True)
	class Meta:
		model = User
		fields = ('id', 'first_name', 'wristband_id', 'phone_no', 'email', 'country_code', 'role', 'gender', 'address', 'longitude', 'latitude', 'image', "user_classes", "is_approved")

class UserUpdateDetialsSerializer(serializers.ModelSerializer):
	"""
	create/update user.
	"""
	id = serializers.IntegerField(required=False)
	user_classes = CreateUpdateUserClassDetailsSerializer(many=True)
	class Meta:
		model = User
		fields = ('id', 'first_name', 'wristband_id', 'phone_no', 'email', 'country_code', 'role', 'gender', 'address', 'longitude', 'latitude', 'image', "user_classes")       

	def update(self, instance, validated_data):
		instance.first_name = validated_data['first_name']
		instance.wristband_id = validated_data['wristband_id']
		instance.email = validated_data['email']
		instance.country_code = validated_data['country_code']
		instance.phone_no = validated_data['phone_no']
		instance.address = validated_data['address']
		if 'longitude' in validated_data:
			instance.longitude = validated_data['longitude']
		if 'latitude' in validated_data:
			instance.latitude = validated_data['latitude']
		instance.gender = validated_data['gender']
		instance.role = validated_data['role']
		instance.image = validated_data['image']
		instance.encoded_id = None
		instance.is_active = True
		instance.profile_status = 4
		instance.save()

		self.update_user_classes(instance, validated_data["user_classes"])

		return instance
	
	def update_user_classes(self, instance, user_classes_data):
		user_classes_ids = []
		for row in user_classes_data:
			if "id" in row:
				user_classes_ids.append(row["id"])
	
		user_class_list = UserClassDetails.objects.filter(user=instance)
		for user_class in user_class_list:
			if user_class.id not in user_classes_ids:
				UserClassDetails.objects.get(id=user_class.id).delete()
		
		for user_class in user_classes_data:
			user_class_id = user_class.get("id")
			try:
				user_class_obj = UserClassDetails.objects.get(id=user_class_id)
				user_class_obj.classes = user_class["classes"]
				user_class_obj.branch = user_class["branch"]
				user_class_obj.save()
				self.update_user_sections(user_class_obj, user_class["user_sections"])
			except UserClassDetails.DoesNotExist:
				sections = user_class.pop("user_sections")
				class_details_obj = UserClassDetails.objects.create(user=instance, **user_class)
				for section_data in sections:
					UserSectionDetails.objects.create(user_class=class_details_obj, **section_data)
		
		return 'success'
	

	def update_user_sections(self, instance, user_sections_data):
		user_sections_ids = []
		for row in user_sections_data:
			if "id" in row:
				user_sections_ids.append(row["id"])
	
		user_sections_list = UserSectionDetails.objects.filter(user_class=instance)
		for user_sections in user_sections_list:
			if user_sections.id not in user_sections_ids:
				UserSectionDetails.objects.get(id=user_sections.id).delete()
		
		for user_sections in user_sections_data:
			user_section_id = user_sections.get("id")
			try:
				user_section_obj = UserSectionDetails.objects.get(id=user_section_id)
				user_section_obj.section = user_sections["section"]
				user_section_obj.save()
			except UserSectionDetails.DoesNotExist:
				UserSectionDetails.objects.create(user_class=instance, **user_sections)
		
		return 'success'