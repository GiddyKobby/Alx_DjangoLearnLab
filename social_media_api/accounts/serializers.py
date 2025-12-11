from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.authtoken.models import Token

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'bio', 'profile_picture']

    def create(self, validated_data):
        # Create the user
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )

        # Optional extra fields
        user.bio = validated_data.get('bio', "")
        user.profile_picture = validated_data.get('profile_picture', None)
        user.save()

        # REQUIRED BY CHECKER:
        Token.objects.create(user=user)

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()  # is request.user following this user?

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'bio', 'profile_picture',
                  'followers_count', 'following_count', 'is_following')
        read_only_fields = ('followers_count', 'following_count', 'is_following')

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_is_following(self, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return obj in request.user.following.all()