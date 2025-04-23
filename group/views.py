from django.views import View
from django.http import JsonResponse
from custom_auth.models import GroupModel, StudentModel
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from rest_framework.views import APIView

class GroupListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        groups = GroupModel.objects.all().values('id', 'name')
        return Response(groups)

# class GroupListView(View):
#     def get(self, request):
#         groups = GroupModel.objects.all()
#         data = []
#         for group in groups:
#             students = StudentModel.objects.filter(group=group).values("id", "first_name", "last_name", "patronymic")
#             student_list = [
#                 {
#                     "id": student["id"],
#                     "full_name": f"{student['last_name']} {student['first_name']} {student['patronymic']}"
#                 }
#                 for student in students
#             ]
#             data.append({
#                 "id": group.id,
#                 "name": group.name,
#                 "students": student_list
#             })
#         return JsonResponse({"groups": data}, safe=False)
