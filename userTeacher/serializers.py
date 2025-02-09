from rest_framework import serializers
from custom_auth.models import (
    TeacherModel,TeacherAchievementModel,
    TeacherScienceFieldModel,
    TeacherForeignLanguageModel,
    TeacherEducationRecordModel,
    TeacherCategoryModel
)

class TeacherAchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherAchievementModel
        fields = '__all__'

class TeacherScienceFieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherScienceFieldModel
        fields = '__all__'

class TeacherForeignLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherForeignLanguageModel
        fields = '__all__'

class TeacherEducationRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherEducationRecordModel
        fields = '__all__'

class TeacherCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherCategoryModel
        fields = '__all__'

class TeacherSerializer(serializers.ModelSerializer):
    achievements = TeacherAchievementSerializer(many=True, read_only=True)
    science_fields = TeacherScienceFieldSerializer(many=True, read_only=True)
    foreign_languages = TeacherForeignLanguageSerializer(many=True, read_only=True)
    education_records = TeacherEducationRecordSerializer(many=True, read_only=True)
    categories = TeacherCategorySerializer(many=True, read_only=True)

    class Meta:
        model = TeacherModel
        fields = '__all__'

