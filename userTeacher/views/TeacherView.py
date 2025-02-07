# userStudent/views/TeacherView.py
"""
В этом файле следующий функционал:
- Просмотр преподавателя. (TeacherView.get)
- Изменение основных данных преподавателя. (TeacherView.put)
"""

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status

from custom_auth.decorator import auth_teacher
from custom_auth.models import TeacherModel


class TeacherView(APIView):
    """
    Преподаватели.
    """
    permission_classes = [AllowAny]

    @auth_teacher
    def get(self, request):
        """
        Просмотр преподавателя. Можно получить полную информацию о преподавателе.
        - fio: {firstName, lastName, patronymic} - ФИО преподавателя
        - iin - ИИН
        - birthDate - Дата рождения
        - nationality - Национальность
        - citizenship - Гражданство
        - gender - Пол
        - maritalStatus - Семейное положение
        - place_of_birth - Место рождения
        - registration_address - Адрес прописки
        - residential_address - Адрес проживания
        """
        
        teacher: TeacherModel = request.user
        
        return Response({"message": "Один преподаватель", "data":{
            "fio": teacher.last_name  + " " + teacher.first_name + " " + teacher.patronymic,
            "iin": teacher.iin,
            "birthDate": teacher.birth_date,
            "nationality": teacher.nationality,
            "citizenship": teacher.citizenship,
            "gender": teacher.gender,
            "maritalStatus": teacher.marital_status,
            "place_of_birth": teacher.place_of_birth,
            "registration_address": teacher.registration_address,
            "residential_address": teacher.residential_address
        }}, status=status.HTTP_200_OK)
        
    @auth_teacher
    def post(self, request):
        
        function = request.query_params.get('function')
        
        if not function:
            return Response({"error": "Function is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if function == 'put':
            return self.put(request)
        else:
            return Response({"error": "Invalid function"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        Изменение основных данных преподавателя. 
        """

        teacher: TeacherModel = request.user
        
        first_name = request.data.get('firstName', None)
        last_name = request.data.get('lastName', None)
        patronymic = request.data.get('patronymic', None)
        residential_address = request.data.get('residentialAddress', None)
        residence_address = request.data.get('residenceAddress', None)
        
        if first_name:
            teacher.first_name = first_name
            teacher.save()
            return Response({"message": "Имя преподавателя изменено"}, status=status.HTTP_200_OK)
        
        elif last_name:
            teacher.last_name = last_name
            teacher.save()
            return Response({"message": "Фамилия преподавателя изменена"}, status=status.HTTP_200_OK)
        
        elif patronymic:
            teacher.patronymic = patronymic
            teacher.save()
            return Response({"message": "Отчество преподавателя изменено"}, status=status.HTTP_200_OK)
        
        elif residential_address:
            teacher.residential_address = residential_address
            teacher.save()
            return Response({"message": "Адрес проживания преподавателя изменен"}, status=status.HTTP_200_OK)
        elif residence_address:
            teacher.registration_address = residence_address
            teacher.save()
            return Response({"message": "Адрес прописки преподавателя изменен"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Параметры не переданы или переданы некорректно"}, status=status.HTTP_400_BAD_REQUEST)
    

