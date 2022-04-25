from rest_framework import serializers
from .models import PostComment, Post


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class PostCommentSerializer(serializers.ModelSerializer):
    answers = RecursiveField(many=True)

    class Meta:
        model = PostComment
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    comments = PostCommentSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'comments')
