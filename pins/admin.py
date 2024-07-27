from django.contrib import admin
from .models import Pin, Comment, CommentReplies, SavePins, LikePins
# Register your models here.

admin.site.register(Pin)
admin.site.register(Comment)
admin.site.register(CommentReplies)
admin.site.register(SavePins)
admin.site.register(LikePins)
