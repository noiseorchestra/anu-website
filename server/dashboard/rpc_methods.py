from modernrpc.core import rpc_method
from modernrpc.auth.basic import http_basic_auth_login_required
from fabric import Connection
from invoke import Responder
from environs import Env
from linode_api4 import LinodeClient
import schedule
import time

env = Env()
env.read_env()

host = env("JACKTRIP_SERVER_ADDRESS", default="123.123.123.123")
username = env("JACKTRIP_SERVER_USER", default="user")
password = env("JACKTRIP_SERVER_PASSWORD", default="password")
token = env("LINODE_PAT", default="")

sudopass = Responder(
    pattern=r'\[sudo\] password for fabric:',
    response=password + '\n',
)

f = open("/root/.ssh/id_rsa.pub", "r")
pkey = f.read().rstrip('\n')
f.close()

client = LinodeClient('{}'.format(token))
c = Connection(host, username, connect_timeout=4, connect_kwargs={
        "key_filename": "/root/.ssh/id_rsa",
    },
)

def _delete_all_servers():
    my_linodes = client.linode.instances()

    for current_linode in my_linodes:
        print("delete: ", current_linode.label)
        current_linode.delete()

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
    if type(q_value) != int:
        print('The input is not a number')
        return "not a number"
    else:
    result = c.run('echo "FPP=%s" > /etc/jacktrip_pypatcher/jackd.conf' % (fpp_value))
    return result.exited


@http_basic_auth_login_required
@rpc_method
def set_q(q_value):
    """
    Set the JackTrip q (buffer) value on a py_patcher server.
    """
    if type(q_value) != int:
        print('The input is not a number')
        return "not a number"
    else:
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


@http_basic_auth_login_required
@rpc_method
def create_server():
    """
    Create a py_patcher server on Linode.
    """

    # Nanode for safety, while developing
    type_id = "g6-nanode-1"
    # type_id = "g6-dedicated-8"
    # curl https://api.linode.com/v4/linode/types | jq '."data"[] | ."label"'

    # London
    region_id = "eu-west"
    image = "linode/ubuntu18.04"

    linode, password = client.linode.instance_create(type_id, region_id,
                            image=image, authorized_keys=pkey)

    if not linode:
        raise RuntimeError("it didn't work")

    return {"ip": linode.ipv4[0]}


@http_basic_auth_login_required
@rpc_method
def fetch_all_servers():
    """
    Fetch all linode server instances
    """
    my_linodes = client.linode.instances()
    ips = []

    if len(my_linodes) == 0:
        return ips

    for current_linode in my_linodes:
        print(current_linode.ipv4[0])
        ips.append(current_linode.ipv4[0])

    return ips


@http_basic_auth_login_required
@rpc_method
def delete_all_servers():
    """
    Delete all linode server instances
    """
    response = "success"
    try:
        _delete_all_servers()
    except AssertionError as error:
        print(error)
        response = error  

    return response

