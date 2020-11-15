from modernrpc.core import rpc_method
from django.contrib.auth.decorators import login_required
from fabric import Connection
import os

host = os.getenv('JACKTRIP_SERVER_ADDRESS')
username = os.getenv('JACKTRIP_SERVER_USER')
password = os.getenv('JACKTRIP_SERVER_PASSWORD')

c = Connection(host, username, connect_kwargs={
        "password": password,
    },)


@login_required
@rpc_method
def get_fpp():
    result = c.run('cat /etc/jacktrip_pypatcher/jackd.conf')
    return result.stdout.strip()


@login_required
@rpc_method
def get_q():
    result = c.run('cat /etc/jacktrip_pypatcher/jacktrip.conf')
    return result.stdout.strip()


@login_required
@rpc_method
def set_fpp(fpp_value):
    result = c.run('echo "FPP=%s" > /etc/jacktrip_pypatcher/jackd.conf' % (fpp_value))
    return result.exited


@login_required
@rpc_method
def set_q(q_value):
    result = c.run('echo "Q=%s" > /etc/jacktrip_pypatcher/jacktrip.conf' % (q_value))
    return result.exited
