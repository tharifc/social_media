from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from twitterapi.serializers import PostsSerializer, UserSerializer, LoginSerializer, UserProfileSerializer
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework import authentication, permissions
from rest_framework.views import APIView
from twitterapi.models import Posts
from rest_framework import status
from twitterapi.models import User, UserProfile


class PostsModelViewSets(ViewSet, ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]
    model = Posts
    serializer_class = PostsSerializer
    queryset = Posts.objects.all()

    def get_queryset(self):
        return Posts.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = PostsSerializer(data=request.data, context={'user': request.user})

        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


class UserCreation(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SigninView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            uname = serializer.validated_data.get("username")
            password = serializer.validated_data.get("password")
            user = authenticate(request, username=uname, password=password)

            if user:
                login(request, user)
                return Response({"msg": "login success"})
            else:
                return Response({"msg": "invalid credentials"})
        else:
            return Response({"msg": "login success"})

    # def get(self, request, *args, **kwargs):
    #     qs = UserProfile.objects.filter(user=request.user)
    #     serializer = UserProfileSerializer(qs)
    #     return Response(serializer.data)


class AddUserProfile(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get(self, request, *args, **kwargs):
        # print(self.request.user)
        userdata = User.objects.get(id=request.user.id)
        userprofiledata = UserProfile.objects.get(user=request.user)
        bio = userprofiledata.bio
        phone = userprofiledata.phone
        udata = UserSerializer(userdata)
        serializer = UserProfileSerializer(userprofiledata)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # print(request.data)
        user_data = UserProfileSerializer(data=request.data, context={'user': request.user})
        if user_data.is_valid():
            user_data.save()
            return Response(user_data.data, status=status.HTTP_201_CREATED)
        else:
            return Response(user_data.errors)
