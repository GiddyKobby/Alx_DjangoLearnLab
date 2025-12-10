from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()


class Meta:
    model = User
    fields = (
        'id', 'username', 'email', 'first_name', 'last_name',
        'bio', 'profile_picture', 'followers_count'
    )
    read_only_fields = ('id', 'followers_count')


def get_followers_count(self, obj):
  return obj.followers.count()




class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)


class Meta:
    model = User
    fields = ('id', 'username', 'email', 'password')


def create(self, validated_data):
    password = validated_data.pop('password')
    user = User(**validated_data)
    user.set_password(password)
    user.save()
# create token
    Token.objects.create(user=user)
    return user




class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)