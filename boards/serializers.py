from rest_framework import serializers
from .models import Board

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'
        
    def create(self, validated_data):
        request = self.context.get('request', None)
        if request:
            validated_data['user'] = request.user
        return super().create(validated_data)