from rest_framework import serializers
from .models import StudentModel, TeacherAchievementModel, TeacherCategoryModel, TeacherEducationRecordModel, TeacherForeignLanguageModel, TeacherGroupModel, TeacherModel, TeacherScienceFieldModel


class CamelCaseModelSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {self.camel_case(k): v for k, v in data.items()}

    def camel_case(self, snake_str):
        parts = snake_str.split('_')
        return parts[0] + ''.join(word.capitalize() for word in parts[1:])

class TeacherSerializer(CamelCaseModelSerializer):
    class Meta:
        model = TeacherModel
        fields = '__all__'

    
class TeacherAchievementSerializer(CamelCaseModelSerializer):
    class Meta:
        model = TeacherAchievementModel
        fields = '__all__'


class TeacherScienceFieldSerializer(CamelCaseModelSerializer):
    class Meta:
        model = TeacherScienceFieldModel
        fields = '__all__'


class TeacherForeignLanguageSerializer(CamelCaseModelSerializer):
    class Meta:
        model = TeacherForeignLanguageModel
        fields = '__all__'


class TeacherEducationRecordSerializer(CamelCaseModelSerializer):
    class Meta:
        model = TeacherEducationRecordModel
        fields = '__all__'


class TeacherCategorySerializer(CamelCaseModelSerializer):
    class Meta:
        model = TeacherCategoryModel
        fields = '__all__'


class TeacherGroupSerializer(CamelCaseModelSerializer):
    group = serializers.SerializerMethodField()

    class Meta:
        model = TeacherGroupModel
        fields = ['id', 'teacher', 'group']

    def get_group(self, obj):
        students = StudentModel.objects.filter(group=obj.group)
        return {
            'id': obj.group.id,
            'name': obj.group.name,
            'students': StudentSerializer(students, many=True).data
        }


class StudentSerializer(serializers.ModelSerializer):
    groupName = serializers.CharField(source='group.name', read_only=True)

    class Meta:
        model = StudentModel
        fields = '__all__'

    def get_groupName(self, obj):
        return obj.group.name if obj.group else None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {self.camel_case(k): v for k, v in data.items()}

    def camel_case(self, snake_str):
        parts = snake_str.split('_')
        return parts[0] + ''.join(word.capitalize() for word in parts[1:])