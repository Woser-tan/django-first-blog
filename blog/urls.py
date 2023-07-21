from blog.views import PostViewSet, CommentViewSet
from rest_framework import renderers
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from django.contrib.auth.decorators import login_required

post_list = PostViewSet.as_view({
    'get' : 'list'
})
post_detail = login_required(PostViewSet.as_view({
    'get' : 'retrieve'
}))
post_new = login_required(PostViewSet.as_view({
    'get' : 'create',
    'post' : 'create'
}))
post_edit = login_required(PostViewSet.as_view({
    'get': 'update',
    'post': 'update'
}))
post_draft_list = login_required(PostViewSet.as_view({
    'get': 'list'
}))
post_publish = login_required(PostViewSet.as_view({
    'get': 'update'
}))
post_remove = login_required(PostViewSet.as_view({
    'get': 'destroy'
}))
add_comment_to_post = login_required(CommentViewSet.as_view({
    'get': 'create',
    'post': 'create'
}))
comment_approve = login_required(CommentViewSet.as_view({
    'get': 'update'
}))
comment_remove = login_required(CommentViewSet.as_view({
    'get': 'destroy'
}))

urlpatterns = format_suffix_patterns([
    path('', post_list, name = 'post_list'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post/new/', login_required(post_new), name='post_new'),
    path('post/<int:pk>/edit/', login_required(post_edit), name='post_edit'),
    path('drafts/', login_required(post_draft_list), name='post_draft_list'),
    path('post/<pk>/publish/', login_required(post_publish), name='post_publish'),
    path('post/<pk>/remove/', login_required(post_remove), name='post_remove'),
    path('post/<int:pk>/comment/', login_required(add_comment_to_post), name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', login_required(comment_approve), name='comment_approve'),
    path('comment/<int:pk>/remove/', login_required(comment_remove), name='comment_remove'),
])