from django.http import Http404
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import status
from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone


class PostList(APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'blog/post_list.html'

    def get(self, request):
        posts = Post.objects.filter(published_date__lte = timezone.now()).order_by('published_date')
        return Response({'posts': posts})


class PostDetail(APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'blog/post_detail.html'

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        post = self.get_object(pk)
        return Response({'post': post})
    

class PostNew(APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = "blog/post_edit.html"

    def post(self, request):
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
        
    def get(self,request):
        form = PostForm()
        return Response({'form': form})
    

class PostEdit(APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = "blog/post_edit.html"

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        post = self.get_object(pk)
        form = PostForm(instance=post)
        return Response({'form': form})
    
    def post(self, request, pk):
        post = self.get_object(pk)
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
        
class PostDraftList(APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = "blog/post_draft_list.html"

    def get(self, request):
        posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
        return Response({'posts': posts})
    

class PostPublish(APIView):

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.publish()
        return redirect('post_detail', pk=pk)
    

class PostRemove(APIView):
    
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post.delete()
        return redirect('post_list')
    
class AddCommentToPost(APIView):

    renderer_classes = [TemplateHTMLRenderer]
    template_name = "blog/add_comment_to_post.html"

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        post = self.get_object(pk)
        form = CommentForm()
        return Response({'form': form})
        
    def post(self, request, pk):
        post = self.get_object(pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
        

class CommentApprove(APIView):
        
    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.approve()
        return redirect('post_detail', pk=comment.post.pk)
    
class CommentRemove(APIView):

    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        comment.delete()
        return redirect('post_detail', pk=comment.post.pk)
