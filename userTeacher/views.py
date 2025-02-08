from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from custom_auth.models import TeacherModel
from .serializers import TeacherModelSerializer
from rest_framework.permissions import AllowAny

class TeacherDetailView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, iin):
        """
        Получение информации о преподавателе по IIN.
        """
        print("*"*100)
        try:
            teacher = TeacherModel.objects.get(iin=iin)
        except TeacherModel.DoesNotExist:
            return Response(
                {"error": "Преподаватель с таким IIN не найден."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = TeacherModelSerializer(teacher)
        return Response(serializer.data)