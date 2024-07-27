from django.urls import path
from .views import BoardListCreate, BoardDetails, AddPinToBoard, FollowedBoardsView

urlpatterns = [
    path('boards/', BoardListCreate.as_view(), name='board-list-create'),
    path('boards/<int:pk>/', BoardDetails.as_view(), name='board-details'),
    path('boards/<int:pk>/add_pin/', AddPinToBoard.as_view(), name='add-pin-to-board'),
    path('boards/followed/', FollowedBoardsView.as_view(), name='followed-boards'),
]
