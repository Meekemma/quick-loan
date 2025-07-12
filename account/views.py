from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import RegistrationSerializer, LoginSerializer, LogoutSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
import logging

User = get_user_model()
logger = logging.getLogger(__name__)


@api_view(['POST'])
def registration_view(request):
    """
    Handles user registration.
    """
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    logger.info(f"New user registered: {serializer.validated_data.get('email')}")
    
    return Response({'message': 'Registration successful'}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login_view(request):
    """
    Handles user login and returns JWT tokens.
    """
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    
    user = serializer.validated_data['user']
    refresh = RefreshToken.for_user(user)

    logger.info(f"User {user.email} logged in successfully")
    
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }, status=status.HTTP_200_OK)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logs out a user by blacklisting their refresh token.
    """
    serializer = LogoutSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    logger.info(f"User {request.user.email} logged out successfully")

    return Response(
        {"message": "Successfully logged out"},
        status=status.HTTP_200_OK
    )
