from django.contrib.auth.models import User
from users.serializers import RegisterSerializer, SignupSerializer, LoginSerializer
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.views import APIView
# Create your views here.

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class SignupView(APIView):
    def post(self, request):
        signup_serializer = SignupSerializer(data=request.data)
        if signup_serializer.is_valid():
            signup_serializer.save()
            return Response(signup_serializer.data, status=status.HTTP_200_OK)
        return Response(signup_serializer.data, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self,request):
        login_serializer = LoginSerializer(data=request.data)
        login_serializer.is_valid(raise_exception=True)
        #validate()의 리턴값인 Token을 받아옴
        token = login_serializer.validated_data
        return Response({"token": token.key}, status=status.HTTP_200_OK)