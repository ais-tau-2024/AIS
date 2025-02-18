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
        instance.patronymic = validated_data.get('patronymic', instance.patronymic)
        instance.nationality = validated_data.get('nationality', instance.nationality)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.citizenship = validated_data.get('citizenship', instance.citizenship)
        instance.marital_status = validated_data.get('marital_status', instance.marital_status)
        instance.place_of_birth = validated_data.get('place_of_birth', instance.place_of_birth)
        instance.document_type = validated_data.get('document_type', instance.document_type)
        instance.document_number = validated_data.get('document_number', instance.document_number)
        instance.document_issue_date = validated_data.get('document_issue_date', instance.document_issue_date)
        instance.document_expiry_date = validated_data.get('document_expiry_date', instance.document_expiry_date)
        instance.issuing_authority = validated_data.get('issuing_authority', instance.issuing_authority)
        instance.registration_address = validated_data.get('registration_address', instance.registration_address)
        instance.residential_address = validated_data.get('residential_address', instance.residential_address)
        instance.home_phone = validated_data.get('home_phone', instance.home_phone)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.email = validated_data.get('email', instance.email)
        instance.teaching_language = validated_data.get('teaching_language', instance.teaching_language)
        instance.profile_photo = validated_data.get('profile_photo', instance.profile_photo)

        # Categories
        instance.category = validated_data.get('category', instance.category)
        instance.order_number = validated_data.get('order_number', instance.order_number)
        instance.order_date = validated_data.get('order_date', instance.order_date)
        instance.confirmation_document = validated_data.get('confirmation_document', instance.confirmation_document)

        # Education_records
        instance.institution_name = validated_data.get('institution_name', instance.institution_name)
        instance.document_details = validated_data.get('document_details', instance.document_details)
        instance.graduation_year = validated_data.get('graduation_year', instance.graduation_year)
        instance.qualification = validated_data.get('qualification', instance.qualification)
        instance.specialization = validated_data.get('specialization', instance.specialization)
        instance.foreign_institution = validated_data.get('foreign_institution', instance.foreign_institution)
        instance.scan_copy = validated_data.get('scan_copy', instance.scan_copy)

        # Foreign_languages
        instance.language = validated_data.get('language', instance.language)
        instance.proficiency_level = validated_data.get('proficiency_level', instance.proficiency_level)

        # Science_fields
        instance.field = validated_data.get('field', instance.field)
        instance.academic_degree = validated_data.get('academic_degree', instance.academic_degree)
        instance.academic_status = validated_data.get('academic_status', instance.academic_status)

        # Achievements
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
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

