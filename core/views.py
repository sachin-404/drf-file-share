from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import File, User
from .serializers import FileSerializer
from rest_framework.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
# from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from .serializers import UserSerializer

class FileUploadView(generics.CreateAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        file = self.request.FILES.get('file')
        allowed_types = ['pptx', 'docx', 'xlsx']
        if file.name.split('.')[-1] not in allowed_types:
            raise ValidationError("Only pptx, docx, and xlsx files are allowed.")
        serializer.save(user=self.request.user)


class FileListView(generics.ListAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return File.objects.filter(user=self.request.user)

class FileDownloadView(generics.RetrieveAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return File.objects.filter(user=self.request.user)

    def get_object(self):
        queryset = self.get_queryset()
        obj = generics.get_object_or_404(queryset, pk=self.kwargs['pk'])
        return obj
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        token = default_token_generator.make_token(request.user)
        uidb64 = urlsafe_base64_encode(instance.pk)
        url = f'/download-file/{uidb64}/{token}/'
        return Response({'download_link': url, 'message': 'success'})

class UserSignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(user.pk)
        verification_link = f'http://localhost:8000/verify-email/{uidb64}/{token}/'
        # send verification email with verification_link
        send_mail(
            'Verify your email',
            f'Click the following link to verify your email: {verification_link}',
            'sachinkant404@gmail.com',
            [user.email],
            fail_silently=False,
        )

class UserLoginView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token = default_token_generator.make_token(user)
        return Response({'token': token}, status=status.HTTP_200_OK)

class UserLogoutView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
