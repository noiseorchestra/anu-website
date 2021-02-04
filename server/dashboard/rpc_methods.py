from modernrpc.core import rpc_method
from modernrpc.auth.basic import http_basic_auth_login_required
from fabric import Connection
from invoke import Responder
from environs import Env

env = Env()
env.read_env()

host = env("JACKTRIP_SERVER_ADDRESS", default="123.123.123.123")
username = env("JACKTRIP_SERVER_USER", default="user")
password = env("JACKTRIP_SERVER_PASSWORD", default="password")

sudopass = Responder(
    pattern=r'\[sudo\] password for fabric:',
    response=password + '\n',
)

c = Connection(host, username, connect_timeout=4, connect_kwargs={"password": password})

@rpc_method
@http_basic_auth_login_required
def get_fpp():
    """
    Fetch the current JACK fpp (frames per period) value from a py_patcher server.
    :return: String
    """
    result = c.run('cat /etc/jacktrip_pypatcher/jackd.conf')
    key, value = result.stdout.strip().split('=')
    return value


@http_basic_auth_login_required
@rpc_method
def get_q():
    """
    Fetch the current JackTrip q (buffer) value from a py_patcher server.
    :return: String
    """
    result = c.run('cat /etc/jacktrip_pypatcher/jacktrip.conf')
    key, value = result.stdout.strip().split('=')
    return value


@http_basic_auth_login_required
@rpc_method
def set_fpp(fpp_value):
    """
    Set the JACK fpp (frames per period) value on a py_patcher server.
    """
    result = c.run('echo "FPP=%s" > /etc/jacktrip_pypatcher/jackd.conf' % (fpp_value))
    return result.exited


@http_basic_auth_login_required
@rpc_method
def set_q(q_value):
    """
    Set the JackTrip q (buffer) value on a py_patcher server.
    """
    result = c.run('echo "Q=%s" > /etc/jacktrip_pypatcher/jacktrip.conf' % (q_value))
    return result.exited


@http_basic_auth_login_required
@rpc_method
def restart_jacktrip():
    """
    Restart JackTrip on a py_patcher server.
    """
    result = c.run('sudo systemctl restart jacktrip.service', pty=True, watchers=[sudopass])
    return result.exited


@http_basic_auth_login_required
@rpc_method
def restart_jackd():
    """
    Restart JACK on a py_patcher server.
    """
    result = c.run('sudo systemctl restart jackd.service', pty=True, watchers=[sudopass])
    return result.exited
