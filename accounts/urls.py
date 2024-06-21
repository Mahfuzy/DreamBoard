from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import Profile, ProfileDetails, UserView, FollowUser, UnfollowUser, FollowersCount, FollowersList, FollowingList, UserDetails, RegisterAPIView, LoginAPIView, LogoutAPIView, FollingCount,  ChatRoomViewSet,  MessageViewSet
router = DefaultRouter()
router.register(r'chatrooms', ChatRoomViewSet)
router.register(r'messages', MessageViewSet)


urlpatterns = [
    path('users/', UserView.as_view(), name='users'),
    path('signup/', RegisterAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('users/<int:pk>/', UserDetails.as_view(), name='user-details'),
    path('profile/', Profile.as_view(), name='profile'),
    path('profile/<int:pk>/', ProfileDetails.as_view(), name='profile-details'),
    path('users/<int:user_id>/follow/', FollowUser.as_view(), name='follow_user'),
    path('users/<int:user_id>/unfollow/', UnfollowUser.as_view(), name='unfollow_user'),
    path('users/<int:user_id>/followers/', FollowersList.as_view(), name='user-followers'),
    path('users/<int:user_id>/following/', FollowingList.as_view(), name='user-following'),
    path('users/followers_count/<int:user_id>/', FollowersCount.as_view(), name='followers-count'),
    path('users/following_count/<int:user_id>/', FollingCount.as_view(), name='following_count')
]
