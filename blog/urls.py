from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.PostView.as_view(view_select='post_list'), name = 'post_list'),
    #path('', views.PostList.as_view(), name = 'post_list'),
    path('post/<int:pk>/', views.PostView.as_view(view_select='post_detail'), name='post_detail'),
    #path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail),
    path('post/new/', login_required(views.PostView.as_view(view_select='post_new')), name='post_new'),
    #path('post/<int:pk>/', views.PostNew.as_view(), name='post_new'),
    path('post/<int:pk>/edit/', login_required(views.PostView.as_view(view_select='post_edit')), name='post_edit'),
    #path('post/<int:pk>/', views.PostEdit.as_view(), name='post_new'),
    path('drafts/', login_required(views.PostView.as_view(view_select='post_draft_list')), name='post_draft_list'),
    #path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail),
    path('post/<pk>/publish/', login_required(views.PostView.as_view(view_select='post_publish')), name='post_publish'),
    #path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail),
    path('post/<pk>/remove/', login_required(views.PostView.as_view(view_select='post_remove')), name='post_remove'),
    #path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail),
    path('post/<int:pk>/comment/', login_required(views.CommentView.as_view(view_select='add_comment_to_post')), name='add_comment_to_post'),
    #path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail),
    path('comment/<int:pk>/approve/', login_required(views.CommentView.as_view(view_select='comment_approve')), name='comment_approve'),
    #path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail),
    path('comment/<int:pk>/remove/', login_required(views.CommentView.as_view(view_select='comment_remove')), name='comment_remove'),
    #path('post/<int:pk>/', views.PostDetail.as_view(), name='post_detail),
]
