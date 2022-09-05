from django.contrib.auth.models import User
#패스워드 검증도구 - 너무쉬운지, 짧은지 다 알아서 걸러줌
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers
from rest_framework.authtoken.models import Token
#이메일 중복방지 용 검증도구
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate


#------------------------------------회원가입-------------------------------------------------------------
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],  # 이메일 중복검증
    )
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],  # 비밀번호 검증
    )
    password2 = serializers.CharField(write_only=True, required=True)  # 비밀번호 확인을 위한 필드

    class Meta:
        model = User
        fields = ("username", "email", "password", "password2")

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'password' : '비밀번호와 비밀번호 확인이 일치하지 않습니다.'}
            )
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            email = validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return user


class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password", "password2")


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True) #읽기만 가능 수정불가하게 함.

    def validate(self, data):
        user = authenticate(**data)
        if user:
            token = Token.objects.get(user=user)
            return token
        raise serializers.ValidationError(
            {'error' : "로그인 불가합니다. 관리자에게 문의하세요"}
        )