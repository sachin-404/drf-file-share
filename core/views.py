from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import File, User
from .serializers import FileSerializer
from rest_framework.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
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
        
        # Check if the user is an Ops User
        if self.request.user.user_type == 'ops':
            serializer.save(user=self.request.user)
        else:
            raise ValidationError("Only Ops Users can upload files.")

class FileListView(generics.ListAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Check if the user is an Ops User or a Client User
        if self.request.user.user_type == 'ops':
            return File.objects.filter(user=self.request.user)
        elif self.request.user.user_type == 'client':
            return File.objects.all()  # Return all files for Client Users
        else:
            return File.objects.none()  # Return empty queryset for other users

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
    queryset = User.objects.all()  # Allow signup for both Ops and Client Users
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        token = default_token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        verification_link = f'http://localhost:8000/verify-email/{uidb64}/{token}/'
        # send verification email with verification_link
        send_mail(
            'Verify your email',
            f'Click the following link to verify your email: {verification_link}',
            'sachinkant404@gmail.com',
            [user.email],
            fail_silently=False,
        )

class VerifyEmailView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        uidb64 = kwargs['uidb64']
        token = kwargs['token']
        try:
            uid = force_bytes(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                user.is_verified = True
                user.save()
                return Response({'message': 'Email verified successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(generics.CreateAPIView):
    queryset = User.objects.all()  # Allow login for both Ops and Client Users
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
