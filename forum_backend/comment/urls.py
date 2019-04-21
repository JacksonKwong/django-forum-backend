from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from comment.views import CommentList

app_name = 'comment'
urlpatterns = format_suffix_patterns([
    path('list/', CommentList.as_view(), name='comment-list'),
])