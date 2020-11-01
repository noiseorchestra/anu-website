from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from .views import HomePageView, PageView
from .models import Page


class HomepageTests(SimpleTestCase):

    def setUp(self):
        url = reverse('')
        self.response = self.client.get(url)

    def test_homepage_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'home.html')

    def test_homepage_contains_correct_html(self):
        self.assertContains(self.response, 'Homepage')

    def test_homepage_does_not_contain_incorrect_html(self):
        self.assertNotContains(
            self.response, 'Hi there! I should not be on the page.')

    def test_homepage_url_resolves_homepageview(self):
        view = resolve('/')
        self.assertEqual(
            view.func.__name__,
            HomePageView.as_view().__name__
        )

class PageTests(TestCase):

    def setUp(self):
        self.page = Page.objects.create(
            title='About',
            slug='about',
            body='Hello, this is some page content',
            nav_position='02',
        )

    def test_page_listing(self):
        self.assertEqual(f'{self.page.title}', 'About')
        self.assertEqual(f'{self.page.slug}', 'about')
        self.assertEqual(f'{self.page.body}', 'Hello, this is some page content')
        self.assertEqual(f'{self.page.nav_position}', '02')

    def test_page_view(self):
        response = self.client.get(self.page.get_absolute_url())
        no_response = self.client.get('/12345/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, 'About')
        self.assertTemplateUsed(response, 'pages/page.html')

    def test_page_url_resolves_pageview(self):
        view = resolve('/pages/about')
        self.assertEqual(
            view.func.__name__,
            PageView.as_view().__name__
        )
