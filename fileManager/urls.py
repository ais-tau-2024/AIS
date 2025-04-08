from django.urls import path
from .views import (
    CreateDesktopView, CreateFolderView, ListTeachersAccessView, ListDesktopsView, DeleteDesktopView,
    GrantAccessView, ListFilesView, RevokeAccessView, UploadFileView, FileActionView
)

urlpatterns = [
    path('desktops/', CreateDesktopView.as_view(), name='create_desktop'),
    path('desktops/list/', ListDesktopsView.as_view(), name='list_desktops'),
    path('desktops/<int:desktop_id>/', DeleteDesktopView.as_view(), name='delete_desktop'),
    path('desktops/<int:desktop_id>/createFolder/', CreateFolderView.as_view(), name='create_folder'),
    path('desktops/<int:desktop_id>/grant/', GrantAccessView.as_view(), name='grant_access'),
    path('desktops/<int:desktop_id>/revoke/', RevokeAccessView.as_view(), name='revoke_access'),
    path('desktops/<int:desktop_id>/files/', ListFilesView.as_view(), name='list_files'),
    path('desktops/<int:desktop_id>/upload/', UploadFileView.as_view(), name='upload_file'),
    path('desktops/<int:desktop_id>/file/', FileActionView.as_view(), name='file_action'),

    path('teachers/available/', ListTeachersAccessView.as_view(), name='available_teachers'),
]


