from django.urls import path
from . import views
from blog.views import PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, PostShareView, CommentCreateView, CommentDeleteView, post_search
from .feeds import LatestPostsFeed

app_name = 'blogs'

urlpatterns = [
    # Example URL pattern
    path('', PostListView.as_view(), name='all'),
    path('post/<int:year>/<int:month>/<int:day>/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),
    path('post/create/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>/share/', PostShareView.as_view(), name='post_share'),
    
    path('post/<int:pk>/comment/', CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    
    path('tag/<slug:tag_slug>/', PostListView.as_view(), name='post_list_by_tag'),
    
    path('feed/', LatestPostsFeed(), name='post_feed'),
    path('search/', views.post_search, name='post_search'),
]
