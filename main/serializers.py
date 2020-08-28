from rest_framework import serializers, status
from rest_framework.response import Response

from authentication.models import User
from .models import Post, Comment, Hashtag


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d %b %Y', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'created_at', 'image']


    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user_id'] = request.user.id
        print(validated_data['title'])
        title = validated_data['title'].split()
        print(title)
        for word in title:
            if word.startswith('#'):
                if Hashtag.objects.filter(tag=word).exists():
                    pass
                else:
                    Hashtag.objects.create(tag=word)
        print(Hashtag.objects.all())
        post = Post.objects.create(**validated_data)
        return post

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.username

        representation['comments'] = instance.comments.count()
        representation['image'] = self.__get_image_url(instance)

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
    created_at = serializers.DateTimeField(format='%d %b %Y', read_only=True)
    parent = serializers.PrimaryKeyRelatedField(queryset=Comment.objects.all(), write_only=True, required=False)

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'created_at', 'parent']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.username
        representation['replies'] = CommentReplySerializer(instance.children.all(), many=True, context=self.context).data
        return representation


class CommentReplySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d %b %Y', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'comment', 'user', 'created_at']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.username
        return representation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']