from rest_framework import serializers
from custom_auth.models import TeacherModel

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