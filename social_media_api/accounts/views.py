from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token
from .serializers import RegisterSerializer, UserSerializer, LoginSerializer
from rest_framework.views import APIView


User = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)


def create(self, request, *args, **kwargs):
   serializer = self.get_serializer(data=request.data)
   serializer.is_valid(raise_exception=True)
   user = serializer.save()
   token = Token.objects.get(user=user)
   data = UserSerializer(user, context={'request': request}).data
   data['token'] = token.key
   return Response(data, status=status.HTTP_201_CREATED)




class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = (permissions.AllowAny,)


def post(self, request, *args, **kwargs):
   serializer = self.get_serializer(data=request.data)
   serializer.is_valid(raise_exception=True)
   username = serializer.validated_data['username']
   password = serializer.validated_data['password']
   user = authenticate(username=username, password=password)
   if not user:
      return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
   token, _ = Token.objects.get_or_create(user=user)
   data = UserSerializer(user, context={'request': request}).data
   data['token'] = token.key
   return Response(data)




class ProfileView(generics.RetrieveUpdateAPIView):
   serializer_class = UserSerializer
   permission_classes = (permissions.IsAuthenticated,)


def get_object(self):
  return self.request.user