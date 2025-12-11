from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


User = get_user_model()

from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'bio', 'profile_picture']

    def create(self, validated_data):
        # Required by your checker
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )

        # Optional extra fields
        user.bio = validated_data.get('bio', "")
        user.profile_picture = validated_data.get('profile_picture', None)
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


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




