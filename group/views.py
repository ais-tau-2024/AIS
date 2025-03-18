from django.views import View
from django.http import JsonResponse
from custom_auth.models import GroupModel, StudentModel

class GroupListView(View):
    def get(self, request):
        groups = GroupModel.objects.all()
        data = []
        for group in groups:
            students = StudentModel.objects.filter(group=group).values("id", "first_name", "last_name", "patronymic")
            student_list = [
                {
                    "id": student["id"],
                    "full_name": f"{student['last_name']} {student['first_name']} {student['patronymic']}"
                }
                for student in students
            ]
            data.append({
                "id": group.id,
                "name": group.name,
                "students": student_list
            })
        return JsonResponse({"groups": data}, safe=False)
