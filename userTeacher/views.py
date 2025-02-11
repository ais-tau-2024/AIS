from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.exceptions import NotFound
from custom_auth.models import TeacherModel
from .serializers import TeacherSerializer

class TeacherDetailByIINView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = TeacherModel.objects.all()
    serializer_class = TeacherSerializer
    lookup_field = 'iin'

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_field]}
        try:
            return queryset.get(**filter_kwargs)
        except TeacherModel.DoesNotExist:
            raise NotFound({"error": "Teacher with the provided IIN not found."})

    
