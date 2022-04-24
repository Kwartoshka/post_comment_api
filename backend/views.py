from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from .serializers import PostSerializer, PostCommentSerializer
from .models import Post, PostComment
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_swagger.views import get_swagger_view

from django.conf.urls import include
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Pastebin API')

class PostGetView(APIView):

    def get(self, request, id):
        try:
            post = Post.objects.prefetch_related('comments').filter(pk=id).first()
            serializer = PostSerializer(post)
            data = {'data': serializer.data}
            status_code = 200
        except ObjectDoesNotExist:
            data = {'data': 'Post does not exist'}
            status_code = 404

        # return JsonResponse({'data':1}, status=status_code)
        return JsonResponse(data, status=status_code)


class PostPostView(APIView):

    def post(self, request):
        title = request.data.get('title')
        post = Post.objects.create(title=title)
        return JsonResponse({"success": f"Article '{post.title}' created successfully"}, status=201)


class PostCommentView(APIView):

    def post(self, request):

        post_id = request.data.get('post')
        text = request.data.get('text')
        comment_id = request.data.get('comment')
        post = None
        comment = None
        try:
            post = Post.objects.get(id=post_id)
        except ObjectDoesNotExist:
            try:
                comment = PostComment.objects.get(id=comment_id)
            except ObjectDoesNotExist:
                return JsonResponse({"fail": f"Post or comment does not exist"}, status=400)
        if not post:
            comment = PostComment.objects.create(comment=comment, text=text)
        else:
            comment = PostComment.objects.create(post=post, text=text)

        return JsonResponse({"success": f"Comment '{comment.id}' created successfully"}, status=201)
