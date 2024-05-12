from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import status

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email_or_phone = request.data.get('email_or_phone')
        password = request.data.get('password')

        if not email_or_phone or not password:
            return Response({"error": "Both email/phone and password are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Attempt to authenticate user
        user = authenticate(username=email_or_phone, password=password)
        if user:
            # Create token manually
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Login successful. Welcome to the JWT Authentication page using React Js and Django!'
            })
        else:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)



class HomeView(APIView):
     
   permission_classes = (IsAuthenticated, )
   def get(self, request):
       content = {'message': 'Welcome to the JWT Authentication page using React Js and Django!'}
       return Response(content)
   
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        refresh_token = request.data.get("refresh_token")
        if refresh_token is None:
            return Response({'error': 'No refresh token provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
# class RegisterView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')
#         if not username or not password:
#             return Response({"error": "Username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

#         if User.objects.filter(username=username).exists():
#             return Response({"error": "Username is already in use"}, status=status.HTTP_409_CONFLICT)

#         user = User.objects.create_user(username=username, password=password)
#         return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email_or_phone = request.data.get('email_or_phone')
        password = request.data.get('password')
        if not email_or_phone or not password:
            return Response({"error": "Email/Phone and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_email(email_or_phone)
            email = email_or_phone
            phone_number = None
        except ValidationError:
            email = None
            phone_number = email_or_phone
            if len(phone_number) < 10 or not phone_number.isdigit():
                return Response({"error": "Invalid phone number"}, status=status.HTTP_400_BAD_REQUEST)

        if email and CustomUser.objects.filter(email=email).exists():
            return Response({"error": "Email is already in use"}, status=status.HTTP_409_CONFLICT)
        
        if phone_number and CustomUser.objects.filter(phone_number=phone_number).exists():
            return Response({"error": "Phone number is already in use"}, status=status.HTTP_409_CONFLICT)

        user = CustomUser.objects.create_user(username=email_or_phone, email=email, phone_number=phone_number, password=password)
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
