from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Page


def get_pages():
    data = Page.objects.all()

    pages = []
    for page in data:
        pages.append({
            'slug': page.slug,
            'title': page.title,
            'body': page.body,
            'nav_position': page.nav_position
          })
    pages.sort(key=lambda x: x.get('nav_position'))
    return pages


def page(request, slug="home"):
    data = Page.objects.all()
    print(data)

    pages = get_pages()

    return render(request, 'pages/page.html', {'data': {'pages': pages, 'slug': slug}})
