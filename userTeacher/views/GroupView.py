

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status

from custom_auth.decorator import auth_teacher
from custom_auth.models import GroupModel, StudentModel

class GroupView(APIView):
    """
    Преподаватели.
    """
    permission_classes = [AllowAny]

    @auth_teacher
    def get(self, request):
        """
        
        """
        
        function = request.query_params.get('function')
        
        if not function:
            return Response({"error": "Function is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if function == 'get_list':
            return self.get_list(request)
        elif function == 'get_group':
            return self.get_group(request)
        else:
            return Response({"error": "Invalid function"}, status=status.HTTP_400_BAD_REQUEST)
    
    def get_group(self, request):
        """
        
        """
        group_id = request.data.get('group_id')

        groups = GroupModel.objects.all()
        response_data = []
        for group in groups:
            students = StudentModel.objects.filter(group=group).values(
                'id', 'first_name', 'last_name'
        )
        response_data.append({
            "group_id": group.id,
            "group_name": group.name,
            "students": list(students)
        })
        
        if not group_id:
            return Response({"error": "Group id is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    def get_list(self, request):
        """
        
        """