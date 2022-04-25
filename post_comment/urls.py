"""post_comment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from backend.views import PostGetView, PostPostView, PostCommentView, GetCommentView, schema_view

urlpatterns = [
    path('api/comment/', PostCommentView.as_view(), name='post_comment'),
    path('api/post/', PostPostView.as_view(), name='post_post'),
    path('api/post/<id>', PostGetView.as_view(), name='get_post'),
    path('api/comment/<id>', GetCommentView.as_view(), name='get_comment'),
    path('admin/', admin.site.urls),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

]
