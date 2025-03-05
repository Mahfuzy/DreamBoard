from django.shortcuts import get_object_or_404
from rest_framework import generics, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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

    @swagger_auto_schema(
        operation_description="Retrieve a list of boards or create a new board.",
        responses={200: BoardSerializer(many=True), 201: BoardSerializer, 400: "Bad Request"}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new board.",
        request_body=BoardSerializer,
        responses={201: BoardSerializer, 400: "Bad Request"}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class BoardDetails(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

    @swagger_auto_schema(
        operation_description="Retrieve, update, or delete a specific board.",
        responses={200: BoardSerializer, 204: "No Content", 400: "Bad Request", 404: "Not Found"}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a specific board.",
        request_body=BoardSerializer,
        responses={200: BoardSerializer, 400: "Bad Request", 404: "Not Found"}
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a specific board.",
        responses={204: "No Content", 400: "Bad Request", 404: "Not Found"}
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class AddPinToBoard(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Add a pin to a specific board.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Pin ID')
            },
            required=['id']
        ),
        responses={200: BoardSerializer, 400: "Bad Request", 404: "Not Found"}
    )
    def post(self, request, pk):
        board = get_object_or_404(Board, pk=pk)
        pin_id = request.data.get("id")

        if not pin_id:
            return Response({"error": "Pin ID is required"}, status=400)

        board.pins.add(pin_id)
        serializer = BoardSerializer(board)
        return Response(serializer.data)
