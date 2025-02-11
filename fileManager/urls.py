# # fileManager/urls.py

# from django.urls import path

# from .views import DirManagerView, FileManagerView


# urlpatterns = [
#     path('dir', DirManagerView.as_view()),
#     path('file', sFileManagerView.as_view()),
# ]


from django.urls import path
from .views import (
    CreateDesktopView, ListDesktopsView, DeleteDesktopView,
    GrantAccessView, ListFilesView, UploadFileView, FileActionView
)

urlpatterns = [
    path('desktops/', CreateDesktopView.as_view(), name='create_desktop'),
    path('desktops/list/', ListDesktopsView.as_view(), name='list_desktops'),
    path('desktops/<int:desktop_id>/', DeleteDesktopView.as_view(), name='delete_desktop'),
    path('desktops/<int:desktop_id>/grant/', GrantAccessView.as_view(), name='grant_access'),
    path('desktops/<int:desktop_id>/files/', ListFilesView.as_view(), name='list_files'),
    path('desktops/<int:desktop_id>/upload/', UploadFileView.as_view(), name='upload_file'),
    path('desktops/<int:desktop_id>/file/', FileActionView.as_view(), name='file_action'),
]


