from django.contrib.auth.mixins import (
                                       LoginRequiredMixin,
                                       PermissionRequiredMixin,
                                       UserPassesTestMixin
                                        )
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.timezone import make_naive
from django.views.generic import View, DetailView, CreateView, UpdateView, DeleteView

from webapp.models import Article, Tag, ArticleLike
from webapp.forms import ArticleForm, BROWSER_DATETIME_FORMAT


class IndexView(View):
    template_name = 'article/index.html'
    context_object_name = 'articles'
    paginate_by = 2
    paginate_orphans = 0
    model = Article
    ordering = ['-created_at']
    search_fields = ['title__icontains', 'author__icontains']

    def get_queryset(self):
        data = super().get_queryset()
        if not self.request.GET.get('is_admin', None):
            data = data.filter(status='moderated')
        return data

class ArticleView(DetailView):
    template_name = 'article/article_view.html'
    model = Article
    paginate_comments_by = 2
    paginate_comments_orphans = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comments, page, is_paginated = self.paginate_comments(self.object)
        context['comments'] = comments
        context['page_obj'] = page
        context['is_paginated'] = is_paginated

        return context

    def paginate_comments(self, article):
        comments = article.comments.all().order_by('-created_at')
        if comments.count() > 0:
            paginator = Paginator(comments, self.paginate_comments_by, orphans=self.paginate_comments_orphans)
            page_number = self.request.GET.get('page', 1)
            page = paginator.get_page(page_number)
            is_paginated = paginator.num_pages > 1
            return page.object_list, page, is_paginated
        else:
            return comments, None, False


class ArticleCreateView(LoginRequiredMixin, CreateView):
    template_name = 'article/article_create.html'
    form_class = ArticleForm
    model = Article

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = self.request.user
        article.save()
        form.save_m2m()
        tag, _ = Tag.objects.get_or_create(name=self.request.user.username)
        article.tags.add(tag)
        return redirect('webapp:article_view', pk=article.pk)


class ArticleUpdateView(PermissionRequiredMixin, UpdateView):
    template_name = 'article/article_update.html'
    form_class = ArticleForm
    model = Article
    permission_required = 'webapp.change_article'

    def has_permission(self):
        article = self.get_object()
        return super().has_permission() or article.author == self.request.user

    def form_valid(self, form):
        article = form.save()
        tag, _ = Tag.objects.get_or_create(name=self.request.user.username)
        article.tags.add(tag)
        return redirect('webapp:article_view', pk=article.pk)


class ArticleDeleteView(UserPassesTestMixin, DeleteView):
    template_name = 'article/article_delete.html'
    model = Article
    success_url = reverse_lazy('webapp:index')

    def test_func(self):
        return self.request.user.has_perm('webapp.delete_article') or \
            self.get_object().author == self.request.user


class ArticleLikeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs.get('pk'))
        like, created = ArticleLike.objects.get_or_create(article=article, user=request.user)
        if created:
            article.like_count += 1
            article.save()
            return HttpResponse(article.like_count)
        else:
            return HttpResponseForbidden()


class ArticleUnLikeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, pk=kwargs.get('pk'))
        like = get_object_or_404(article.likes, user=request.user)
        like.delete()
        article.like_count -= 1
        article.save()
        return HttpResponse(article.like_count)