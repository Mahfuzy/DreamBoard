from rest_framework import serializers
from .models import Pin, Comment, CommentReplies, LikePins, SavePins
from accounts.serializers import UserSerializer

class LikePinsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikePins
        fields = ['user', 'pin']
        
    def create(self, validated_data):
        request = self.context.get('request', None)
        if request:
            validated_data['user'] = request.user
        return super().create(validated_data)

class SavePinsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavePins
        fields = ['user', 'pin']
        
    def create(self, validated_data):
        request = self.context.get('request', None)
        if request:
            validated_data['user'] = request.user
        return super().create(validated_data)


class CommentRepliesSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()

    class Meta:
        model = CommentReplies
        fields = ['id', 'comment', 'user', 'content', 'created_date', 'parent_reply', 'replies']

    def get_replies(self, obj):
        return CommentRepliesSerializer(obj.replies.all(), many=True).data
    
    def create(self, validated_data):
        request = self.context.get('request', None)
        if request:
            validated_data['user'] = request.user
        return super().create(validated_data)

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    replies = CommentRepliesSerializer(many=True, read_only=True)
    replies_count = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'pin', 'user', 'content', 'created_date', 'replies', 'replies_count']
        
    def get_replies_count(self, obj):
        return obj.replies.count()
    def create(self, validated_data):
        request = self.context.get('request', None)
        if request:
            validated_data['user'] = request.user
        return super().create(validated_data)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not data['replies']:
            data['replies'] = []  # If there are no replies, return an empty list
        return data


class PinSerializer(serializers.ModelSerializer):
    user =  UserSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    saves_count = serializers.SerializerMethodField()
    class Meta:
        model = Pin
        fields = [
            'id', 'title', 'user', 'description', 'link', 'board', 'image', 'video', 'date_created',
             'comments', 'comments_count', 'likes_count', 'saves_count'
        ]
    def create(self, validated_data):
        request = self.context.get('request', None)
        if request:
            validated_data['user'] = request.user
        return super().create(validated_data)
    
    def get_comments_count(self, obj):
        return obj.comments.count()
    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_saves_count(self, obj):
        return obj.savepins_set.count()

    def validate(self, data):
        if data['title'] == '':
            raise serializers.ValidationError("Title cannot be empty.")
        return data