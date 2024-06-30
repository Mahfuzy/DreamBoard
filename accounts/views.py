from django.shortcuts import render, get_object_or_404
from rest_framework import views, generics, status,  viewsets
from rest_framework.response import Response
from .models import Follow, Profile as UserProfile, User, Message,  ChatRoom
from .serializers import ProfileSerializer, UserSerializer, RegisterSerializer, ChatRoomSerializer, MessageSerializer, ChangePasswordSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.authentication import JWTAuthentication

class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
class LogoutAPIView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = get_user_model()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            
            # Change the password
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()

            # Optionally, return a new JWT token
            refresh = RefreshToken.for_user(self.object)
            return Response({
                'message': 'Password changed successfully.',
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetails(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_object(self):
        return self.request.user

class Profile(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer

class ProfileDetails(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer

class FollowersList(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        followers = Follow.objects.filter(followed_user=user)
        followers_users = [follow.follower for follow in followers]
        serializer = UserSerializer(followers_users, many=True)
        return Response(serializer.data)

class FollowingList(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        following = Follow.objects.filter(follower=user)
        following_users = [follow.followed_user for follow in following]
        serializer = UserSerializer(following_users, many=True)
        return Response(serializer.data)

class FollowUser(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, user_id):
        user_to_follow = get_object_or_404(User, pk=user_id)
        if Follow.objects.filter(follower=request.user, followed_user=user_to_follow).exists():
            return Response({'message': 'You are already following this user'}, status=status.HTTP_400_BAD_REQUEST)
        Follow.objects.create(follower=request.user, followed_user=user_to_follow)
        return Response({'message': 'User followed successfully'}, status=status.HTTP_201_CREATED)

class UnfollowUser(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def delete(self, request, user_id):
        user_to_unfollow = get_object_or_404(User, pk=user_id)
        follow = get_object_or_404(Follow, follower=request.user, followed_user=user_to_unfollow)
        follow.delete()
        return Response({'message': 'User unfollowed successfully'}, status=status.HTTP_204_NO_CONTENT)

class FollowersCount(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        followers_count = user.followers.count()
        return Response({'followers_count': followers_count}, status=status.HTTP_200_OK)
    
class FollingCount(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        following_count = user.following.count()
        return Response({'following_count': following_count}, status=status.HTTP_200_OK)
    
class ChatRoomViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = ChatRoom.objects.all().order_by('-created_at')
    serializer_class = ChatRoomSerializer

class MessageViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Message.objects.all().order_by('-timestamp')
    serializer_class = MessageSerializer
