from rest_framework import serializers
from custom_auth.models import (
    TeacherModel, TeacherAchievementModel,
    TeacherScienceFieldModel, TeacherForeignLanguageModel,
    TeacherEducationRecordModel, TeacherCategoryModel
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
    achievements = TeacherAchievementSerializer(many=True, required=False)
    science_fields = TeacherScienceFieldSerializer(many=True, required=False)
    foreign_languages = TeacherForeignLanguageSerializer(many=True, required=False)
    education_records = TeacherEducationRecordSerializer(many=True, required=False)
    categories = TeacherCategorySerializer(many=True, required=False)

    class Meta:
        model = TeacherModel
        fields = '__all__'

    def update(self, instance, validated_data):
        # Обновление связанных данных
        achievements_data = validated_data.pop('achievements', [])
        science_fields_data = validated_data.pop('science_fields', [])
        foreign_languages_data = validated_data.pop('foreign_languages', [])
        education_records_data = validated_data.pop('education_records', [])
        categories_data = validated_data.pop('categories', [])

        # Обновление основной модели
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Обновление достижений
        if achievements_data:
            instance.achievements.all().delete()
            for achievement_data in achievements_data:
                TeacherAchievementModel.objects.create(teacher=instance, **achievement_data)

        # Обновление научных направлений
        if science_fields_data:
            instance.science_fields.all().delete()
            for science_field_data in science_fields_data:
                TeacherScienceFieldModel.objects.create(teacher=instance, **science_field_data)

        # Обновление языков
        if foreign_languages_data:
            instance.foreign_languages.all().delete()
            for language_data in foreign_languages_data:
                TeacherForeignLanguageModel.objects.create(teacher=instance, **language_data)

        # Обновление образования
        if education_records_data:
            instance.education_records.all().delete()
            for education_data in education_records_data:
                TeacherEducationRecordModel.objects.create(teacher=instance, **education_data)

        # Обновление категорий
        if categories_data:
            instance.categories.all().delete()
            for category_data in categories_data:
                TeacherCategoryModel.objects.create(teacher=instance, **category_data)

        return instance