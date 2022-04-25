from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from .serializers import PostCommentSerializer, PostSerializer
from .models import Post, PostComment
from django.core.exceptions import ObjectDoesNotExist


from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema



schema_view = get_schema_view(
   openapi.Info(
      title="Post and comment API",
      default_version='v1',
      description="Test description",
      terms_of_service="",
      contact=openapi.Contact(email="contact@contact.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)



def answers_builder(comments, post=None, current_comment=None, depth=1, limit=3, no_limit=False):
    if no_limit:
        limit += 1
    if depth <= limit:
        if post:
            local_comments = comments.filter(post=post.id)
        elif current_comment:
            local_comments = comments.filter(comment=current_comment.id)

        if not local_comments:
            return []
        else:
            answers_list = []
            for comment in local_comments:
                text = comment.text
                id = comment.id
                answers = answers_builder(comments,
                                          current_comment=comment,
                                          depth=depth+1,
                                          limit=limit,
                                          no_limit=no_limit)
                answers_list.append({'id': id,
                        'text': text,
                        'answers': answers})
            return answers_list
    else:
        local_comments = comments.filter(comment=current_comment.id)
        return list(local_comments.values('id').distinct())


class PostGetView(APIView):

    def get(self, request, id):
        try:
            post = Post.objects.filter(pk=id).first()
            comments = PostComment.objects.all()
            data = {'data':
                        {'id': post.id,
                         'title': post.title,
                         'comments': answers_builder(comments, post=post)}}
            status_code = 200
        except ObjectDoesNotExist:
            data = {'data': 'Post does not exist'}
            status_code = 404
        return JsonResponse(data, status=status_code)


class PostPostView(APIView):

    title_param_config = openapi.Parameter('title',
                              in_=openapi.IN_QUERY,
                              description="Title of Post",
                              type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[title_param_config])
    def post(self, request):
        title = request.data.get('title')
        if not title:
            title = request.query_params['title']
        post = Post.objects.create(title=title)
        return JsonResponse({"success": f"Article '{post.title} (id {post.id})' created successfully"}, status=201)


class PostCommentView(APIView):

    post_param_config = openapi.Parameter('post',
                                           in_=openapi.IN_QUERY,
                                           description="id of post",
                                           type=openapi.TYPE_INTEGER)
    comment_param_config = openapi.Parameter('comment',
                                          in_=openapi.IN_QUERY,
                                          description="id of comment",
                                          type=openapi.TYPE_INTEGER)

    text_param_config = openapi.Parameter('text',
                                             in_=openapi.IN_QUERY,
                                             description="text of comment",
                                             type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[post_param_config,
                                            comment_param_config,
                                            text_param_config
                                            ])
    def post(self, request):

        post_id = request.data.get('post')
        if not post_id:
            post_id = request.query_params.get('post')

        text = request.data.get('text')
        if not text:
            text = request.query_params.get('text')
        if not text:
            return JsonResponse({"fail": f"You should provide text of comment"}, status=400)

        comment_id = request.data.get('comment')
        if not comment_id:
            comment_id = request.query_params.get('comment')

        if post_id and comment_id:
            return JsonResponse({"fail": f"You should provide post or comment only"}, status=400)

        if post_id:
            try:
                post = Post.objects.get(id=post_id)
                new_comment = PostComment.objects.create(post=post, text=text)
            except ObjectDoesNotExist:
                return JsonResponse({"fail": f"Post does not exist"}, status=400)
        elif comment_id:
            try:
                comment = PostComment.objects.get(id=comment_id)
                new_comment = PostComment.objects.create(comment=comment, text=text)
            except ObjectDoesNotExist:
                return JsonResponse({"fail": f"Comment does not exist"}, status=400)
        return JsonResponse({"success": f"Comment '{new_comment.id}' created successfully"}, status=201)


class GetCommentView(APIView):

    def get(self, request, id):

        try:
            comment = PostComment.objects.get(id=id)
            serializer = PostCommentSerializer(comment)
            data = serializer.data
            status_code = 200
            return JsonResponse(data, status=status_code)
        except ObjectDoesNotExist:
            return JsonResponse({"fail": f"Comment does not exist"}, status=400)
