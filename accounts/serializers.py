from rest_framework import serializers
from .models import Follow, User

class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ('id', 'email', 'username','profile_pic', 'bio', 'website', 'followers_count', 'following_count')
        
    def get_followers_count(self, obj):
        return Follow.objects.filter(followed_user=obj).count()
    
    def get_following_count(self, obj):
        return Follow.objects.filter(follower=obj).count()
        
        
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class FollowSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)
    followed_user = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ['follower', 'followed_user', 'created_at']
        
