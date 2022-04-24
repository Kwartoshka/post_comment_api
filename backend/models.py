from django.db import models

# Create your models here.


class Post(models.Model):

    title = models.CharField(max_length=128, blank=True, null=True)


class PostComment(models.Model):
    comment = models.ForeignKey('PostComment', on_delete=models.CASCADE, related_name='answers', null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', null=True)
    text = models.TextField()

