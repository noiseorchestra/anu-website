from modernrpc.core import rpc_method
from modernrpc.auth.basic import http_basic_auth_login_required
from fabric import Connection
import paramiko
from invoke import Responder
from environs import Env
from linode_api4 import LinodeClient
import schedule
import time
import os

env = Env()
env.read_env()

LINODE_PAT = env("LINODE_PAT", default="")
MAX_LINODES = env("MAX_LINODES", default=0)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

f = open("/root/.ssh/id_rsa.pub", "r")
public_key = f.read().rstrip('\n')
f.close()

private_key = paramiko.rsakey.RSAKey.from_private_key_file(filename="/root/.ssh/id_rsa")

client = LinodeClient('{}'.format(LINODE_PAT))

def _get_fabric_client(host):
    return Connection(host, "root", connect_kwargs={
        "pkey": private_key,
        },
    )

def _delete_all_servers():

    my_linodes = client.linode.instances()

    if len(my_linodes) == 0:
        return "no linodes to delete"
    else:
        for current_linode in my_linodes:
            print("delete: ", current_linode.label)
            current_linode.delete()
        return "deleted all linodes"


def _upload_files(c, dir_path):
    for filename in os.listdir(dir_path):
        print('Upload: {}/{}'.format(dir_path, filename))
        result = c.put('{}/{}'.format(dir_path, filename))
        print("Uploaded {0.local} to {0.remote}".format(result))

def _run_scripts(c):
    c.run('./install.sh && reboot')


@rpc_method
@http_basic_auth_login_required
def get_fpp(host):
    """
    Fetch the current JACK fpp (frames per period) value from a py_patcher server.
    :return: String
    """
    result = _get_fabric_client(host).run('cat /etc/jacktrip_pypatcher/jackd.conf')
    key, value = result.stdout.strip().split('=')
    return value


@http_basic_auth_login_required
@rpc_method
def get_q(host):
    """
    Fetch the current JackTrip q (buffer) value from a py_patcher server.
    :return: String
    """
    result = _get_fabric_client(host).run('cat /etc/jacktrip_pypatcher/jacktrip.conf')
    key, value = result.stdout.strip().split('=')
    return value


@http_basic_auth_login_required
@rpc_method
def set_fpp(host, fpp_value):
    """
    Set the JACK fpp (frames per period) value on a py_patcher server.
    """
    if type(fpp_value) == int:
        result = _get_fabric_client(host).run('echo "FPP=%s" > /etc/jacktrip_pypatcher/jackd.conf' % (fpp_value))
        return result.exited
    return "not a number"


@http_basic_auth_login_required
@rpc_method
def set_q(host, q_value):
    """
    Set the JackTrip q (buffer) value on a py_patcher server.
    """
    if type(q_value) == int or q_value == "auto":
        result = _get_fabric_client(host).run('echo "Q=%s" > /etc/jacktrip_pypatcher/jacktrip.conf' % (q_value))
        return result.exited
    return "not a valid q value"


@http_basic_auth_login_required
@rpc_method
def restart_jacktrip(host):
    """
    Restart JackTrip on a py_patcher server.
    """
    result = _get_fabric_client(host).run('sudo systemctl restart jacktrip.service')
    return result.exited


@http_basic_auth_login_required
@rpc_method
def restart_jackd(host):
    """
    Restart JACK on a py_patcher server.
    """
    result = _get_fabric_client(host).run('sudo systemctl restart jackd.service')
    return result.exited


@http_basic_auth_login_required
@rpc_method
def create_server():
    """
    Create a py_patcher server on Linode.
    """

    my_linodes = client.linode.instances()
    if len(my_linodes) >= MAX_LINODES:
        raise RuntimeError("max server number of {} reached".format(MAX_LINODES))

    # Nanode for safety, while developing
    type_id = "g6-nanode-1"
    # type_id = "g6-dedicated-8"
    # curl https://api.linode.com/v4/linode/types | jq '."data"[] | ."label"'

    # London
    region_id = "eu-west"
    image = "linode/ubuntu18.04"

    linode, password = client.linode.instance_create(type_id, region_id,
                            image=image, authorized_keys=public_key)

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
    response = _delete_all_servers()

    return response

@http_basic_auth_login_required
@rpc_method
def upload_everything_and_run(host):
    # Check if custom darkice config exists
    # Change this to genuine file

    scripts_path = os.path.join(BASE_DIR, 'dashboard/jacktrip-server-automation/scripts')
    templates_path = os.path.join(BASE_DIR, 'dashboard/jacktrip-server-automation/templates')

    if os.path.isfile('{}/darkice.cfg'.format(templates_path)):
        print ("Darkice config found")
    else:
        raise RuntimeError("Please create custom darkice config file")

    c = _get_fabric_client(host)

    print("Upload files")

    _upload_files(c, scripts_path)
    _upload_files(c, templates_path)

    result = c.put('{}/darkice.cfg'.format(templates_path))
    print("Uploaded {0.local} to {0.remote}".format(result))

    _run_scripts(c)

    return "success"
