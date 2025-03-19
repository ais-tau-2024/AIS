# custom_auth/decorator.py

from functools import wraps
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status

# from custom_auth.models import AdminAuthTokenModel
from custom_auth.models import TeacherAuthTokenModel


def auth_teacher(func):
    """
    Декоратор для аутентификации преподавателя. В headers записывается данные о преподавателя: headers.user
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            token = args[1].headers['Auth']
        except Exception as e:
            print(e)
            return Response({"error": "Authentication token required"}, status=status.HTTP_401_UNAUTHORIZED) 


        if not token:
            return Response({"error": "Authentication token required"}, status=status.HTTP_401_UNAUTHORIZED) 
        
        # Проверка на существование токена
        db_token = TeacherAuthTokenModel.objects.filter(token=token).first()
        if not db_token:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Проверка на соответствие токена
        if token != db_token.token:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

        args[1].user = db_token.teacher
        args[1].user_type = 'teacher'

        return func(*args, **kwargs)

    return wrapper

