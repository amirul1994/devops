from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import SignupSerializer, SearchSerializer, LoginSerializer
#from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from django.contrib.auth import  login
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from .backends import CustomUserBackend
#from django.contrib.auth.hashers import make_password
from django.http import JsonResponse


# signup view
@api_view(['POST'])
def data_signup(request):
    if request.method == 'POST':
        serializer = SignupSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save() # save into db
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

# login view
@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def data_login(request):
    # if request.method == 'POST':
    # retrieve value of name and password from db
    name = request.data.get('name')
    password = request.data.get('password')

    print(f'Name: {name}')
    print(f'Password: {password}')

    user = CustomUserBackend().authenticate(request, name=name, password=password)
    
    print(f'User: {user}')
    
    #verify name & password
    if user is not None:
        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        serializer = LoginSerializer(user)
        return Response({'user': serializer.data, 'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


# search view
@api_view(['GET'])
def data_search(request):
    if request.method == 'GET':
        try:
         name = request.GET.get('name')
         user = CustomUser.objects.get(name=name)
         serializer = SearchSerializer(user)
         
         return Response(
               serializer.data,
               status=status.HTTP_200_OK
               )
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as exception:
            return Response({'error': str(exception)}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error':'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)