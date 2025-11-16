from django.shortcuts import render

# advanced_features_and_security/views.py

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import Article


@permission_required('advanced_features_and_security.can_view', raise_exception=True)
def article_list(request):
    articles = Article.objects.all()
    return render(request, 'articles/list.html', {'articles': articles})


@permission_required('advanced_features_and_security.can_create', raise_exception=True)
def article_create(request):
    return render(request, 'articles/create.html')  # placeholder


@permission_required('advanced_features_and_security.can_edit', raise_exception=True)
def article_edit(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'articles/edit.html', {'article': article})


@permission_required('advanced_features_and_security.can_delete', raise_exception=True)
def article_delete(request, pk):
    return render(request, 'articles/delete.html')

