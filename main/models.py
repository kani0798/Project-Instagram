from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.


class Post(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='posts')
    title = models.TextField()
    tag = models.ManyToManyField('Hashtag', blank=True, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(get_user_model(), blank=True, related_name='likers')
    image = models.ImageField(upload_to='posts', blank=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.comment


class Hashtag(models.Model):
    tag = models.SlugField(max_length=150, primary_key=True)

    def __str__(self):
        return self.tag


