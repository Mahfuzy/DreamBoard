from django.urls import path
from .views import UserView, FollowUser, UnfollowUser, FollowersCount, FollowersList, FollowingList, UserDetails, RegisterAPIView, LogoutAPIView, FollowingCount, ChangePasswordView,ActivateAPIView, LoginAPIView

urlpatterns = [
    path('users/', UserView.as_view(), name='users'),
    path('signup/', RegisterAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('activate/<uidb64>/<token>/', ActivateAPIView.as_view(), name='activate'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('users/<str:username>/', UserDetails.as_view(), name='user-details'),
    path('users/<str:username>/follow/', FollowUser.as_view(), name='follow_user'),
    path('users/<str:username>/unfollow/', UnfollowUser.as_view(), name='unfollow_user'),
    path('users/<str:username>/followers/', FollowersList.as_view(), name='user-followers'),
    path('users/<str:username>/following/', FollowingList.as_view(), name='user-following'),
]