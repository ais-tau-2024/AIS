from rest_framework import serializers
from .models import StudentModel, TeacherModel

class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherModel
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {self.camel_case(k): v for k, v in data.items()}

    def camel_case(self, snake_str):
        parts = snake_str.split('_')
        return parts[0] + ''.join(word.capitalize() for word in parts[1:])
    

class StudentSerializer(serializers.ModelSerializer):
    groupName = serializers.SerializerMethodField()

    class Meta:
        model = StudentModel
        fields = '__all__'  # Или явно указать: ['id', 'first_name', ..., 'group', 'groupName']

    def get_groupName(self, obj):
        return obj.group.name if obj.group else None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {self.camel_case(k): v for k, v in data.items()}

    def camel_case(self, snake_str):
        parts = snake_str.split('_')
        return parts[0] + ''.join(word.capitalize() for word in parts[1:])