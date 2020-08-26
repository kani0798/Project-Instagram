from rest_framework import serializers, status
from rest_framework.response import Response

from .models import Post, Comment, Hashtag


class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d %b %Y', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'created_at', 'image']

    def create(self, validated_data):
        request = self.context.get('request')

        validated_data['user_id'] = request.user.id

        post = Post.objects.create(**validated_data)
        return post

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.username
        representation['comments'] = CommentSerializer(instance.comments.all(), many=True, context=self.context).data
        representation['image'] = self.__get_image_url(instance)
        print(instance.likes.all())
        representation['likes'] = instance.likes.all().count()

        return representation

    def __get_image_url(self, instance):
        request = self.context.get('request')
        if instance.image:
            url = instance.image.url
            if request is not None:
                url = request.build_absolute_uri(url)
        else:
            url = ''
        return url


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'created_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.username
        return representation

