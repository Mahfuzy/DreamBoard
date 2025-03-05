from django.shortcuts import render, get_object_or_404
from rest_framework import views, generics, status, viewsets
from rest_framework.response import Response
from .models import Follow, User
from .serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str, force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Register a new user and send verification email.",
        request_body=RegisterSerializer,
        responses={201: "Created", 400: "Bad Request"}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        user = serializer.save(is_active=False)
        self.send_verification_email(user)

    def send_verification_email(self, user):
        mail_subject = 'Activate your account'
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        activation_link = f"http://localhost:3000/accounts/activate/{uid}/{token}"
        message = f"Hi {user.username},\n\n" \
                f"Thanks for signing up! Please click the link below to verify your email address and activate your account:\n\n" \
                f"{activation_link}\n\n" \
                f"Best regards,\nYour Team"
        send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [user.email])

class ActivateAPIView(views.APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="Activate a user account via email confirmation.",
        responses={200: "Account activated successfully!", 400: "Invalid activation link."}
    )
    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Account activated successfully!'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Activation link is invalid!'}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(views.APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_description="User login endpoint.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING)
            },
            required=['email', 'password']
        ),
        responses={200: "Login successful", 401: "Invalid credentials or inactive account"}
    )
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            if not user.is_active:
                return Response({'detail': 'Account is not active. Please verify your email.'}, status=status.HTTP_401_UNAUTHORIZED)

            refresh = RefreshToken.for_user(user)
            response = Response({
                'detail': 'Login successful',
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            }, status=status.HTTP_200_OK)

            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                samesite='None',
                secure=True,
            )

            response.set_cookie(
                key='access_token',
                value=str(refresh.access_token),
                httponly=True,
                samesite='None',
                secure=True,
            )
            return response
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutAPIView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="User logout endpoint.",
        responses={200: "Logout successful", 400: "Invalid request"}
    )
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()

            response = Response({'detail': 'Logout successful'}, status=status.HTTP_200_OK)
            response.delete_cookie('refresh_token')
            response.delete_cookie('access_token')
            return response
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
