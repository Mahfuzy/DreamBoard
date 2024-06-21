from django.shortcuts import render, get_object_or_404
from rest_framework import views, generics, status,  viewsets
from rest_framework.response import Response
from .models import Follow, Profile as UserProfile, User, Message,  ChatRoom
from .serializers import ProfileSerializer, UserSerializer, RegisterSerializer, ChatRoomSerializer, MessageSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import permissions
from django.contrib.auth import authenticate, login

class RegisterAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class LoginAPIView(views.APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        user = authenticate(email=email, password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token
            
            response = Response({
                'refresh': str(refresh),
                'access': str(access_token)
            }, status=status.HTTP_200_OK)
            
            response.set_cookie(
                key='access_token',
                value=str(access_token),
                httponly=True,
                secure=True,
                samesite='Strict'
            )
            response.set_cookie(
                key='refresh_token',
                value=str(refresh),
                httponly=True,
                secure=True,
                samesite='Strict'
            )
            return response
        else:
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
    
class LogoutAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
class UserView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    def get_object(self):
        return self.request.user

class Profile(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer

class ProfileDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = UserProfile.objects.all()
    serializer_class = ProfileSerializer

class FollowersList(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        followers = Follow.objects.filter(followed_user=user)
        followers_users = [follow.follower for follow in followers]
        serializer = UserSerializer(followers_users, many=True)
        return Response(serializer.data)

class FollowingList(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        following = Follow.objects.filter(follower=user)
        following_users = [follow.followed_user for follow in following]
        serializer = UserSerializer(following_users, many=True)
        return Response(serializer.data)

class FollowUser(views.APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, user_id):
        user_to_follow = get_object_or_404(User, pk=user_id)
        if Follow.objects.filter(follower=request.user, followed_user=user_to_follow).exists():
            return Response({'message': 'You are already following this user'}, status=status.HTTP_400_BAD_REQUEST)
        Follow.objects.create(follower=request.user, followed_user=user_to_follow)
        return Response({'message': 'User followed successfully'}, status=status.HTTP_201_CREATED)

class UnfollowUser(views.APIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, user_id):
        user_to_unfollow = get_object_or_404(User, pk=user_id)
        follow = get_object_or_404(Follow, follower=request.user, followed_user=user_to_unfollow)
        follow.delete()
        return Response({'message': 'User unfollowed successfully'}, status=status.HTTP_204_NO_CONTENT)

class FollowersCount(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        followers_count = user.followers.count()
        return Response({'followers_count': followers_count}, status=status.HTTP_200_OK)
    
class FollingCount(views.APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        following_count = user.following.count()
        return Response({'following_count': following_count}, status=status.HTTP_200_OK)
    
class ChatRoomViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = ChatRoom.objects.all().order_by('-created_at')
    serializer_class = ChatRoomSerializer

class MessageViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Message.objects.all().order_by('-timestamp')
    serializer_class = MessageSerializer
