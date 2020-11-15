from modernrpc.core import rpc_method
from modernrpc.auth.basic import http_basic_auth_login_required
from fabric import Connection
from invoke import Responder
import os

host = os.getenv('JACKTRIP_SERVER_ADDRESS')
username = os.getenv('JACKTRIP_SERVER_USER')
password = os.getenv('JACKTRIP_SERVER_PASSWORD')

sudopass = Responder(
    pattern=r'\[sudo\] password:',
    response=password + '\n',
)

c = Connection(host, username, connect_kwargs={"password": password,})


@rpc_method
@http_basic_auth_login_required
def get_fpp():
    result = c.run('cat /etc/jacktrip_pypatcher/jackd.conf')
    return result.stdout.strip()


@http_basic_auth_login_required
@rpc_method
def get_q():
    result = c.run('cat /etc/jacktrip_pypatcher/jacktrip.conf')
    return result.stdout.strip()


@http_basic_auth_login_required
@rpc_method
def set_fpp(fpp_value):
    result = c.run('echo "FPP=%s" > /etc/jacktrip_pypatcher/jackd.conf' % (fpp_value))
    return result.exited


@http_basic_auth_login_required
@rpc_method
def set_q(q_value):
    result = c.run('echo "Q=%s" > /etc/jacktrip_pypatcher/jacktrip.conf' % (q_value))
    return result.exited


@http_basic_auth_login_required
@rpc_method
def restart_jacktrip():
    result = c.run('sudo whoami', pty=True, watchers=[sudopass])
    return result.stdout.strip()
