from django.urls import path, re_path
from core.views import FileUploadView, FileListView, FileDownloadView, UserSignUpView, UserLoginView, UserLogoutView, VerifyEmailView

urlpatterns = [
    path('upload-file/', FileUploadView.as_view(), name='upload_file'),
    path('list-files/', FileListView.as_view(), name='list_files'),
    path('download-file/<int:pk>/', FileDownloadView.as_view(), name='download_file'),
    path('signup/', UserSignUpView.as_view(), name='signup'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    re_path(r'^verify-email/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', VerifyEmailView.as_view(), name='verify_email'),
]