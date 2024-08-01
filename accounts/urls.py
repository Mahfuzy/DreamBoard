from django.urls import path
from .views import UserView, FollowUser, UnfollowUser, FollowersList, FollowingList, UserDetails, RegisterAPIView, LogoutAPIView, ChangePasswordView,ActivateAPIView, LoginAPIView

urlpatterns = [
    path('users/', UserView.as_view(), name='users'),
    path('signup/', RegisterAPIView.as_view(), name='signup'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('activate/<uidb64>/<token>/', ActivateAPIView.as_view(), name='activate'),
    path('logout/', LogoutAPIView.as_view(), name='logout'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('user/<str:username>/', UserDetails.as_view(), name='user-details'),
    path('user/<str:username>/follow/', FollowUser.as_view(), name='follow_user'),
    path('user/<str:username>/unfollow/', UnfollowUser.as_view(), name='unfollow_user'),
    path('user/<str:username>/followers/', FollowersList.as_view(), name='user-followers'),
    path('user/<str:username>/following/', FollowingList.as_view(), name='user-following'),
]