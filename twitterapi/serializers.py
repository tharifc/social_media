from rest_framework.serializers import ModelSerializer
from twitterapi.models import Posts, UserProfile

from rest_framework import serializers
from django.contrib.auth.models import User


class PostsSerializer(ModelSerializer):
    user = serializers.CharField(read_only=True)
    id = serializers.CharField(read_only=True)

    class Meta:
        model = Posts
        exclude = ["liked_by"]

    #
    def create(self, validated_data):
        user = self.context.get('user')
        return Posts.objects.create(**validated_data, user=user)


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "password", "email"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


# class UserProfileSerializer(ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = ["user", "profile_pic", "bio", "phone", "date_of_birth"]


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'phone']

    def create(self, validated_data):
        user = self.context.get('user')
        return UserProfile.objects.create(**validated_data, user=user)
