from rest_framework import serializers
from custom_auth.models import (
    TeacherModel,TeacherAchievementModel,
    TeacherScienceFieldModel,
    TeacherForeignLanguageModel,
    TeacherEducationRecordModel,
    TeacherCategoryModel
)

class TeacherModelSerializer(serializers.ModelSerializer):
    # Добавляем поле для URL фотографии профиля
    profile_photo_url = serializers.SerializerMethodField()

    class Meta:
        model = TeacherModel
        fields = [
            'iin',
            'first_name',
            'last_name',
            'patronymic',
            'nationality',
            'gender',
            'birth_date',
            'citizenship',
            'marital_status',
            'place_of_birth',
            'document_type',
            'document_number',
            'document_issue_date',
            'document_expiry_date',
            'issuing_authority',
            'registration_address',
            'residential_address',
            'home_phone',
            'phone_number',
            'email',
            'teaching_language',
            'profile_photo',
            'profile_photo_url',  # Добавляем URL фотографии
        ]
        read_only_fields = ['profile_photo_url']  # Поле только для чтения

    # Метод для получения URL фотографии профиля
    def get_profile_photo_url(self, obj):
        if obj.profile_photo and hasattr(obj.profile_photo, 'url'):
            return obj.profile_photo.url
        return None

class TeacherAchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherAchievementModel
        fields = ['title', 'description']

class TeacherScienceFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherScienceFieldModel
        fields = ['field', 'academic_degree', 'academic_status']

class TeacherForeignLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherForeignLanguageModel
        fields = ['language', 'proficiency_level']

class TeacherEducationRecordSerializer(serializers.ModelSerializer):
    scan_copy_url = serializers.SerializerMethodField()

    class Meta:
        model = TeacherEducationRecordModel
        fields = [
            'institution_name',
            'document_details',
            'graduation_year',
            'qualification',
            'specialization',
            'foreign_institution',
            'scan_copy',
            'scan_copy_url',
        ]
        read_only_fields = ['scan_copy_url']

    def get_scan_copy_url(self, obj):
        if obj.scan_copy and hasattr(obj.scan_copy, 'url'):
            return obj.scan_copy.url
        return None

class TeacherCategorySerializer(serializers.ModelSerializer):
    confirmation_document_url = serializers.SerializerMethodField()

    class Meta:
        model = TeacherCategoryModel
        fields = [
            'category',
            'order_number',
            'order_date',
            'confirmation_document',
            'confirmation_document_url',
        ]
        read_only_fields = ['confirmation_document_url']

    def get_confirmation_document_url(self, obj):
        if obj.confirmation_document and hasattr(obj.confirmation_document, 'url'):
            return obj.confirmation_document.url
        return None

