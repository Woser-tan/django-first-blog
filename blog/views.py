from django.http import Http404
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import viewsets
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from django.urls import resolve

class PostViewSet(viewsets.ModelViewSet):

    renderer_classes = [TemplateHTMLRenderer]
    
    def list(self, request):
        if resolve(request.path_info).url_name == 'post_draft_list':
            posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
            return Response({'posts': posts}, template_name='blog/post_draft_list.html')
        else:
            posts = Post.objects.filter(published_date__lte = timezone.now()).order_by('published_date')
        return Response({'posts': posts}, template_name='blog/post_list.html')
    
    def retrieve(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        return Response({'post': post}, template_name='blog/post_detail.html')
        
    def create(self, request):
        if request.method == 'POST':
            form = PostForm(request.POST)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            form = PostForm()
        return Response({'form': form}, template_name="blog/post_edit.html")
        
    def update(self, request, pk):
        if request.method == 'POST':
            post = get_object_or_404(Post, pk=pk)
            form = PostForm(request.POST, instance=post)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('post_detail', pk=post.pk)
        else:
            post = get_object_or_404(Post, pk=pk)
            if resolve(request.path_info).url_name == 'post_publish':
                post.publish()
                return redirect('post_detail', pk=pk)
            form = PostForm(instance=post)
        return Response({'form': form}, template_name="blog/post_edit.html")
    
    def destroy(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return redirect('post_list')

class CommentViewSet(viewsets.ModelViewSet):

    renderer_classes = [TemplateHTMLRenderer]

    def create(self, request, pk):
        if request.method == 'POST':
            post = get_object_or_404(Post, pk=pk)
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.save()
                return redirect('post_detail', pk=post.pk)
        else:
            post = get_object_or_404(Post, pk=pk)
            form = CommentForm()

        return Response({'form': form}, template_name="blog/add_comment_to_post.html")
    
    def update(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.approve()
        return redirect('post_detail', pk=comment.post.pk)
    
    def destroy(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return redirect('post_detail', pk=comment.post.pk)