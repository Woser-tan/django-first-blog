from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.PostList.as_view(), name = 'post_list'),
    path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('post/new/', login_required(views.PostNew.as_view()), name='post_new'),
    path('post/<int:pk>/edit/', login_required(views.PostEdit.as_view()), name='post_edit'),
    path('drafts/', login_required(views.PostDraftList.as_view()), name='post_draft_list'),
    path('post/<pk>/publish/', login_required(views.PostPublish.as_view()), name='post_publish'),
    path('post/<pk>/remove/', login_required(views.PostRemove.as_view()), name='post_remove'),
    path('post/<int:pk>/comment/', login_required(views.AddCommentToPost.as_view()), name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', login_required(views.CommentApprove.as_view()), name='comment_approve'),
    path('comment/<int:pk>/remove/', login_required(views.CommentRemove.as_view()), name='comment_remove'),
]