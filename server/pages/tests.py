from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from .views import page
from .models import Page


class PageTests(TestCase):

    def setUp(self):
        self.page = Page.objects.create(
            title='About',
            slug='about',
            body='Hello, this is some page content',
            nav_position='02',
        )
        self.page.save()

    def test_page_listing(self):
        self.assertEqual(f'{self.page.title}', 'About')
        self.assertEqual(f'{self.page.slug}', 'about')
        self.assertEqual(f'{self.page.body}', 'Hello, this is some page content')
        self.assertEqual(f'{self.page.nav_position}', '02')

    def test_page_view(self):
        response = self.client.get(self.page.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'About')
        self.assertTemplateUsed(response, 'pages/page.html')

    def test_page_url_resolves_pageview(self):
        view = resolve('/about/')
        self.assertEqual(
            view.func.__name__,
            page.__name__
        )
