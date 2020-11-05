from django.test import SimpleTestCase, TestCase
from django.urls import reverse, resolve
from .views import page
from .models import NoiseAudioWeb


class PageTests(TestCase):

    def setUp(self):
        self.naw = NoiseAudioWeb.objects.create(
            name='Noise Audio Web',
            slug='noise-audio-web',
            about='All about audio webs',
            owner='Noise Orchestra',
            jacktrip_hub_server='234.234.234.234',
            influxdb='123.123.123.123',
            stream_address='address_of_stream',
            file_storage='to_file_storage'
        )
        self.naw.save()

    def test_page_listing(self):
        self.assertEqual(f'{self.naw.name}', 'Noise Audio Web')
        self.assertEqual(f'{self.naw.slug}', 'about')
        self.assertEqual(f'{self.naw.about}', 'All about audio webs')
        self.assertEqual(f'{self.naw.owner}', 'Noise Orchestra')
        self.assertEqual(f'{self.naw.jacktrip_hub_server}', '234.234.234.234')
        self.assertEqual(f'{self.naw.influxdb}', '123.123.123.123')
        self.assertEqual(f'{self.naw.stream_address}', 'address_of_stream')
        self.assertEqual(f'{self.naw.file_storage}', 'to_file_storage')

    def test_page_view(self):
        response = self.client.get(self.dashboard.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Noise Audio Web')
        self.assertTemplateUsed(response, 'dashboard/page.html')

    def test_page_url_resolves_pageview(self):
        view = resolve('/about/')
        self.assertEqual(
            view.func.__name__,
            page.__name__
        )
