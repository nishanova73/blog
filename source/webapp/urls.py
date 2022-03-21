from django.urls import path
from django.views.generic import RedirectView
from webapp.views import(
                        IndexView,
                        ArticleCreateView,
                        ArticleView,
                        ArticleUpdateView,
                        ArticleDeleteView,
                        ArticleCommentCreateView,
                        CommentUpdateView,
                        CommentDeleteView,
                        ArticleLikeView,
                        ArticleUnLikeView,
                        CommentUnLikeView,
                        CommentLikeView)

app_name = 'webapp'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('articles/', RedirectView.as_view(pattern_name="index")),
    path('articles/add/', ArticleCreateView.as_view(), name='article_create'),
    path('article/<int:pk>/', ArticleView.as_view(), name='article_view'),
    path('article/<int:pk>/update/', ArticleUpdateView.as_view(), name='article_update'),
    path('article/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
    path('article/<int:pk>/comments/add/', ArticleCommentCreateView.as_view(), name='article_comment_add'),
    path('article/<int:pk>/like/', ArticleLikeView.as_view(), name='article_like'),
    path('article/<int:pk>/unlike/', ArticleUnLikeView.as_view(), name='article_unlike'),
    path('comment/<int:pk>/update/', CommentUpdateView.as_view(), name='comment_update'),
    path('comment/<int:pk>/delete/', CommentDeleteView.as_view(), name='comment_delete'),
    path('comment/<int:pk>/like/', CommentLikeView.as_view(), name='comment_like'),
    path('comment/<int:pk>/unlike/', CommentUnLikeView.as_view(), name='comment_unlike'),
]