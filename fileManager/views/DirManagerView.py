# fileManager/views/DirManagerView.py
"""
В этом файле следующий функционал:
- Создание папки по пути и названию. (DirManagerView.create_folder)
- Получение списка файлов и папок по пути. (DirManagerView.get_list)
- Переименование папки по пути и названию папки. (DirManagerView.rename_folder)
- Удаление папки по пути. (DirManagerView.delete_folder)
"""

import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from custom_auth.decorator import auth_teacher
from fileManager.views.helper import FileManager


class DirManagerView(APIView):
    permission_classes = [AllowAny]

    @auth_teacher
    def post(self, request):
        """
        Метод выполняет различные действия в зависимости от параметра `function`:
        - get_list: Получение списка файлов и папок
        - create_folder: Создание новой папки
        - rename_folder: Переименование существующей папки
        - delete_folder: Удаление папки
        """
        
        function = request.query_params.get('function')
        
        if not function:
            return Response({"error": "Function is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if function == 'get_list':
            return self.get_list(request)
        elif function == 'create_folder':
            return self.create_folder(request)
        elif function == 'rename_folder':
            return self.rename_folder(request)
        elif function == 'delete_folder':
            return self.delete_folder(request)
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
    
    def create_folder(self, request):    
        """
        Создает новую папку в указанном пути.
        """
        
        try:
            iin = self.get_iin(request)
        except AttributeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        path = request.data.get('path')
        name = request.data.get('name')
        
        if not name:
            return Response({"error": "Name is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not path and path != '':
            return Response({"error": "Path is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        file_manager = FileManager(iin)
        
        try:
            success = file_manager.create_directory(path, name)
            if success:
                return Response({
                    "message": "Folder successfully created",
                    "content": {
                        "name": name,
                        "type": "folder",
                        "path": os.path.join(path, name)
                    }
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Folder already exists"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "An unexpected error occurred. " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get_list(self, request):
        """
        Получает список файлов и папок по указанному пути.
        """
        try:
            iin = self.get_iin(request)
        except AttributeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        path = request.data.get('path', '')
        
        file_manager = FileManager(iin)
        
        try:
            structure = file_manager.get_directory_structure(path)
            return Response({
                "message": "Files and folders successfully received",
                "content": structure
            }, status=status.HTTP_200_OK)
        except ValueError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def rename_folder(self, request):
        """
        Переименовывает существующую папку.
        """
        try:
            iin = self.get_iin(request)
        except AttributeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        path = request.data.get('path')
        name = request.data.get('name')
        new_name = request.data.get('new_name')
        
        if not name:
            return Response({"error": "Current folder name (`name`) is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not new_name:
            return Response({"error": "New folder name (`new_name`) is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not path and path != '':
            return Response({"error": "Path is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        file_manager = FileManager(iin)
        
        try:
            success = file_manager.rename_directory(path, name, new_name)
            if success:
                return Response({"message": "Folder successfully renamed"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Folder does not exist or renaming failed"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def delete_folder(self, request):
        """
        Удаляет папку и все её содержимое.
        """
        try:
            iin = self.get_iin(request)
        except AttributeError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        path = request.data.get('path')
        name = request.data.get('name')
        
        if not name:
            return Response({"error": "Folder name (`name`) is required"}, status=status.HTTP_400_BAD_REQUEST)

        if not path and path != '':
            return Response({"error": "Path is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        file_manager = FileManager(iin)
        
        try:
            success = file_manager.delete_directory(path, name)
            if success:
                return Response({"message": "Folder successfully deleted"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Folder does not exist or deletion failed"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "An unexpected error occurred."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
