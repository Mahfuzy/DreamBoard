from django.shortcuts import get_object_or_404
from rest_framework import generics, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Board
from .serializers import BoardSerializer
from .filters import BoardFilter
from accounts.models import Follow

class BoardListCreate(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    filterset_class = BoardFilter

class BoardDetails(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

class AddPinToBoard(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        board = get_object_or_404(Board, pk=pk)
        pin_id = request.data.get("id")

        if not pin_id:
            return Response({"error": "Pin ID is required"}, status=400)

        board.pins.add(pin_id)
        serializer = BoardSerializer(board)
        return Response(serializer.data)

class FollowedBoardsView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        current_user = request.user
        followed_user_ids = Follow.objects.filter(follower=current_user).values_list('followed_user_id', flat=True)
        boards = Board.objects.filter(user_id__in=followed_user_ids)
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)
