from django.test import TestCase
from django.urls import resolve
from .views import dashboard
from .models import NoiseAudioWeb
from django.contrib.auth import get_user_model


class DashboardTests(TestCase):

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

        User = get_user_model()
        self.user = User.objects.create_user(
            username='username',
            email='email@email.com',
            password='password'
        )
        self.user.save()

    def test_dashboard_listing(self):
        self.assertEqual(f'{self.naw.name}', 'Noise Audio Web')
        self.assertEqual(f'{self.naw.slug}', 'noise-audio-web')
        self.assertEqual(f'{self.naw.about}', 'All about audio webs')
        self.assertEqual(f'{self.naw.owner}', 'Noise Orchestra')
        self.assertEqual(f'{self.naw.jacktrip_hub_server}', '234.234.234.234')
        self.assertEqual(f'{self.naw.influxdb}', '123.123.123.123')
        self.assertEqual(f'{self.naw.stream_address}', 'address_of_stream')
        self.assertEqual(f'{self.naw.file_storage}', 'to_file_storage')

    def test_dashboard_view_not_authorised(self):
        response = self.client.get(self.naw.get_absolute_url())
        self.assertEqual(response.status_code, 302)

    def test_dashboard_view_is_authorised(self):
        self.client.login(username='username', password='password')
        response = self.client.get(self.naw.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Noise Audio Web')
        self.assertTemplateUsed(response, 'dashboard/dashboard.html')

    def test_dashboard_url_resolves_pageview(self):
        view = resolve('/dashboard/noise-audio-web/')
        self.assertEqual(
            view.func.__name__,
            dashboard.__name__
        )
