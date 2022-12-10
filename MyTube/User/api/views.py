from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from .serializers import LogoutSerializer, LoginSerializer, RegisterSerializer, UserSerializer
from User.models import User
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permissions_class = [permissions.IsAuthenticated,]

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user =User.objects.get(email = user_data['email'])
        token = RefreshToken.for_user(user).access_token
        print(token)
        return Response(user_data, status = status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_class = [permissions.IsAuthenticated,]
    def post(self, request):
         serializer = self.serializer_class(data = request.data)
         serializer.is_valid(raise_exception=True)
         serializer.save()

         return Response(status=status.HTTP_204_NO_CONTENT)
