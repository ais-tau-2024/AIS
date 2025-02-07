# fileManager/views/FileManagerView.py

import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from custom_auth.decorator import auth_teacher
from fileManager.views.helper import FileManager  # Убедитесь, что путь правильный

class FileManagerView(APIView):
    permission_classes = [AllowAny]
    
    @auth_teacher
    def post(self, request):
        """
        Метод выполняет различные действия в зависимости от параметра `function`:
        - add_file: Создание нового файла
        - delete: Удаление файла
        - put: Перезапись содержимого файла
        - rename_file: Переименование существующего файла
        """
        
        function = request.query_params.get('function')
        
        if not function:
            return Response({"error": "Function is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if function == 'add_file':
            return self.add_file(request)
        elif function == 'delete_file':
            return self.delete_file(request)
        elif function == 'rename_file':
            return self.rename_file(request)
        else:
            return Response({"error": "Invalid function"}, status=status.HTTP_400_BAD_REQUEST)
    
    def get_iin(self, request):
        """
        Метод для получения `iin` пользователя.
        Предполагается, что `iin` доступен через `request.user.iin`.
        Измените этот метод в соответствии с вашей логикой получения `iin`.
        """
        user = request.user
        if hasattr(user, 'iin'):
            return user.iin
        raise AttributeError("User does not have 'iin' attribute")
    
    def add_file(self, request):
        """
        Загружает файл в указанный путь.
        Если файл уже существует, он будет заменен, и возвращается статус 200.
        """
        try:
            iin = self.get_iin(request)
        except AttributeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        path = request.data.get('path')
        file_obj = request.FILES.get('file')
        
        if not file_obj:
            return Response({"error": "File is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if path is None:
            return Response({"error": "Path is required"}, status=status.HTTP_400_BAD_REQUEST)

        file_manager = FileManager(iin)
        
        try:
            full_file_path = file_manager._get_full_path(os.path.join(path, file_obj.name))
            file_exists = os.path.exists(full_file_path)  # Проверяем, существует ли файл
            
            # Добавляем/перезаписываем файл
            file_manager.add_file(path, file_obj)
            
            status_code = status.HTTP_200_OK if file_exists else status.HTTP_201_CREATED
            message = "File successfully replaced" if file_exists else "File successfully uploaded"
            
            return Response({
                "message": message,
                "content": {
                    "name": file_obj.name,
                    "type": "file",
                    "path": os.path.join(path, file_obj.name)
                }
            }, status=status_code)
        except ValueError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete_file(self, request):
        """
        Удаляет файл по указанному пути.
        """
        try:
            iin = self.get_iin(request)
        except AttributeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        path = request.data.get('path')
        name = request.data.get('name')
        
        if not name:
            return Response({"error": "File name (`name`) is required"}, status=status.HTTP_400_BAD_REQUEST)

        if path is None:
            return Response({"error": "Path is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        file_manager = FileManager(iin)
        
        try:
            success = file_manager.delete_file(path, name)
            print(success)
            if success or success == []:
                return Response({"message": "File successfully deleted", "content": success}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "File does not exist or deletion failed"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def rename_file(self, request):
        """
        Переименовывает существующий файл.
        """
        try:
            iin = self.get_iin(request)
        except AttributeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        path = request.data.get('path')
        old_name = request.data.get('name')
        new_name = request.data.get('new_name')
        
        if not old_name:
            return Response({"error": "Current file name (`name`) is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not new_name:
            return Response({"error": "New file name (`new_name`) is required"}, status=status.HTTP_400_BAD_REQUEST)

        if path is None:
            return Response({"error": "Path is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        file_manager = FileManager(iin)
        
        try:
            success = file_manager.rename_file(path, old_name, new_name)
            if success or success == []:
                return Response({"message": "File successfully renamed"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "File does not exist or renaming failed"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
