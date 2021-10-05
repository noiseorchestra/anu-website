from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Page    

def set_nav_children(this_page, pages):
    nav_children = []
    
    for page in pages:
        if page['nav_parents'] == this_page['title']:
            nav_children.append(page)
    
    this_page['nav_children'] = nav_children
    return this_page

def get_pages():
    
    pages_data = Page.objects.all()
    
    pages = []
    
    pages.append({
        'slug': 'home',
        'title': 'Home',
        'body': '',
        'nav_position': '01',
        'nav_parents': 'none',
        'nav_children': []
    })
    
    pages.append({
        'slug': 'about',
        'title': 'About',
        'body': '',
        'nav_position': '01',
        'nav_parents': 'none',
        'nav_children': []

    })
    
    pages.append({
        'slug': 'how-to',
        'title': 'How To',
        'body': '',
        'nav_position': '01',
        'nav_parents': 'none',
        'nav_children': []
    })
    
    pages.append({
        'slug': 'listen',
        'title': 'Listen',
        'body': '',
        'nav_position': '01',
        'nav_parents': 'none',
        'nav_children': []
    })
    for page in pages_data:            
        pages.append({
            'slug': page.slug,
            'title': page.title,
            'body': page.body,
            'nav_position': page.nav_position,
            'nav_parents': page.nav_parents,
            'nav_children': []
            })

    pages.sort(key=lambda x: x.get('nav_position'))

    pages_with_nav_children = list(map(lambda x: set_nav_children(x, pages), pages))

    return pages_with_nav_children


def page(request, slug="home"):
    data = Page.objects.all()
    print(data)

    pages = get_pages()

    return render(request, 'pages/page.html', {'data': {'pages': pages, 'slug': slug}})
