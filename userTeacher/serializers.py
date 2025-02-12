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

###############################################################################

class TeacherAchievementUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherAchievementModel
        fields = '__all__'

class TeacherScienceFieldUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherScienceFieldModel
        fields = '__all__'

class TeacherForeignLanguageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherForeignLanguageModel
        fields = '__all__'

class TeacherEducationRecordUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherEducationRecordModel
        fields = '__all__'

class TeacherCategoryUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherCategoryModel
        fields = '__all__'

###################################################################################

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
        # Обновление основных данных преподавателя
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        # TODO ... другие поля ...

        # Сохранение обновленных данных
        instance.save()
        
        # Обновление связанных данных (достижения, научные направления и т.д.)
        self.update_related_data(instance, validated_data)

        return instance

    def update_related_data(self, instance, validated_data):
        # Обновление достижений
        if 'achievements' in validated_data:
            achievements_data = validated_data.pop('achievements')
            self.update_achievements(instance, achievements_data)

        # Обновление научных направлений
        if 'science_fields' in validated_data:
            science_fields_data = validated_data.pop('science_fields')
            self.update_science_fields(instance, science_fields_data)

        # Обновление иностранных языков
        if 'foreign_languages' in validated_data:
            foreign_languages_data = validated_data.pop('foreign_languages')
            self.update_foreign_languages(instance, foreign_languages_data)

        # Обновление записей об образовании
        if 'education_records' in validated_data:
            education_records_data = validated_data.pop('education_records')
            self.update_education_records(instance, education_records_data)

        # Обновление категорий
        if 'categories' in validated_data:
            categories_data = validated_data.pop('categories')
            self.update_categories(instance, categories_data)

    def update_achievements(self, instance, achievements_data):
        # Удаление старых достижений
        instance.achievements.all().delete()
        # Создание новых достижений
        for achievement_data in achievements_data:
            TeacherAchievementModel.objects.create(teacher=instance, **achievement_data)

    def update_science_fields(self, instance, science_fields_data):
        instance.science_fields.all().delete()
        for science_field_data in science_fields_data:
            TeacherScienceFieldModel.objects.create(teacher=instance, **science_field_data)

    def update_foreign_languages(self, instance, foreign_languages_data):
        instance.foreign_languages.all().delete()
        for foreign_language_data in foreign_languages_data:
            TeacherForeignLanguageModel.objects.create(teacher=instance, **foreign_language_data)

    def update_education_records(self, instance, education_records_data):
        instance.education_records.all().delete()
        for education_record_data in education_records_data:
            TeacherEducationRecordModel.objects.create(teacher=instance, **education_record_data)

    def update_categories(self, instance, categories_data):
        instance.categories.all().delete()
        for category_data in categories_data:
            TeacherCategoryModel.objects.create(teacher=instance, **category_data)

