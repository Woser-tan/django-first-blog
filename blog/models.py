from django.db import models
from django.conf import settings
from django.utils import timezone


# Create your models here.

class ApprovedComment(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(approved_comment=True)


class Post(models.Model):

    author         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title          = models.CharField(max_length=200)
    text           = models.TextField()
    created_date   = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    
    def publish(self):

        self.published_date = timezone.now()
        self.save()

    def __str__(self):

        return self.title

    def approved_comments(self):

        return self.comments.all_approved_comments


class Comment(models.Model):

    post                  = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author                = models.CharField(max_length=200)
    text                  = models.TextField()
    created_date          = models.DateTimeField(default=timezone.now)
    approved_comment      = models.BooleanField (default=False)

    all_comments = models.Manager()
    all_approved_comments = ApprovedComment()


    def approve(self):

        self.approved_comment = True
        self.save()


    def __str__(self):

        return self.text