from django.db import models

# Create your models here.
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone


STATUS_CHOICES = [
    ('new', 'NOt moderated'),
    ('moderated', 'Moderated'),
    ('rejected', 'Rejected')
]


class Article(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name='Title',
                             validators=[MinLengthValidator(10)])
    text = models.TextField(max_length=3000, null=False, blank=False, verbose_name='Text')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_DEFAULT, default=1,
                               related_name='articles', verbose_name='Author')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='new', verbose_name='Moderation')
    tags = models.ManyToManyField('webapp.Tag', related_name='articles', blank=True, verbose_name='Tags')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date created')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Date updated')
    like_count = models.IntegerField(verbose_name="Likes", default=0)

    def liked_by(self, user):
        likes = self.likes.filter(user=user)
        return likes.count() > 0

    def __str__(self):
        return "{}. {}".format(self.pk, self.title)

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'


class Comment(models.Model):
    article = models.ForeignKey('webapp.Article', related_name='comments',
                                on_delete=models.CASCADE, verbose_name='Article')
    text = models.TextField(max_length=400, verbose_name='Comment')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_DEFAULT, default=1,
                               related_name='comments', verbose_name='Author')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date created')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Date updated')
    comm_like_count = models.IntegerField(verbose_name="Likes", default=0)

    def __str__(self):
        return self.text[:20]

    def liked_by(self, user):
        likes = self.likes.filter(user=user)
        return likes.count() > 0

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'


class Tag(models.Model):
    name = models.CharField(max_length=31, verbose_name='Тег')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Date created')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'


class ArticleLike(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             related_name='article_likes', verbose_name='User')
    article = models.ForeignKey('webapp.Article', on_delete=models.CASCADE,
                                related_name='likes', verbose_name='Article')

    def __str__(self):
        return f'{self.user.username} - {self.article.title}'

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Article likes'



class CommentLike(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             related_name='comment_likes', verbose_name='User')
    comment = models.ForeignKey('webapp.Comment', on_delete=models.CASCADE,
                                related_name='likes', verbose_name='Comment')

    def __str__(self):
        return f'{self.user.username} - {self.comment.text}'

    class Meta:
        verbose_name = 'Like'
        verbose_name_plural = 'Comment likes'