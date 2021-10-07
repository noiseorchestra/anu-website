from django.test import TestCase
from django.urls import resolve
from unittest.mock import Mock
from .views import dashboard
from .models import NoiseAudioWeb
from django.contrib.auth import get_user_model
from  .rpc_methods import (_check_exit_string, _upload_files, _check_max_linode_instances, _get_all_ips, _check_server_status, _delete_all_servers, _delete_one_server, _read_config_file)
import os

class DashboardTests(TestCase):

# View tests

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

# API tests

    def test_check_max_linode_instances(self):
        self.assertRaises(RuntimeError, _check_max_linode_instances, ["one", "two"], 1)
        self.assertRaises(RuntimeError, _check_max_linode_instances, ["one", "two"], 2)
        _check_max_linode_instances(["one", "two"], 3)
    
    def test_get_all_ips(self):
        self.assertRaises(RuntimeError, _get_all_ips, [])
        linode = Mock(ipv4=["123,123,123,123"])
        ips = _get_all_ips([linode])
        self.assertEqual(ips, ["123,123,123,123"])

    def test_check_server_status(self):
        with self.assertRaises(RuntimeError, msg="No servers running, try creating one first"):
            _check_server_status([], "123,123,123,123")
        linode = Mock(ipv4=["234.234.234.234"])
        with self.assertRaises(RuntimeError, msg="Could not find server with this ip 234.234.234.234"):
            _check_server_status([linode], "123,123,123,123")
        linode = Mock(ipv4=["123,123,123,123"], status="running")
        status = _check_server_status([linode], "123,123,123,123")
        self.assertEqual(status, "running")

    def test_delete_all_servers(self):
        with self.assertRaises(RuntimeError, msg="No linodes to delete"):
            _delete_all_servers([])
        linode1 = Mock(spec=["delete"], label="linode1")
        linode2 = Mock(spec=["delete"], label="linode1")
        response = _delete_all_servers([linode1, linode2])
        self.assertEqual(response, "deleted all linodes")
        linode1.delete.assert_called()
        linode2.delete.assert_called()    
        
    def test_delete_one_server(self):
        with self.assertRaises(RuntimeError, msg="No linodes to delete"):
            _delete_one_server([], "123.123.123.123")
        linode1 = Mock(spec=["delete"], label="linode1", ipv4=["234.234.234.234"])
        with self.assertRaises(RuntimeError, msg="Could not find server with this ip 123.123.123.123"):
            _delete_one_server([], "123.123.123.123")
        linode1 = Mock(spec=["delete"], label="linode1", ipv4=["123.123.123.123"])
        response = _delete_one_server([linode1], "123.123.123.123")
        self.assertEqual(response, "deleted 123.123.123.123")
        linode1.delete.assert_called()

    def test_read_config_file(self):
        result = Mock(stdout="first_key=1\nsecond_key=2\nthird_key=3")
        value = _read_config_file(result, "first_key")
        self.assertEqual(value, "1")
        value = _read_config_file(result, "second_key")
        self.assertEqual(value, "2")
        value = _read_config_file(result, "third_key")
        self.assertEqual(value, "3")
