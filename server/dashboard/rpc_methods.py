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

# hard coded path to script files folder
SERVER_SCRIPTS_PATH = "/app/storage/jacktrip-server-automation"
LINODE_PAT = env("LINODE_PAT", default="")
MAX_LINODES = env("MAX_LINODES", default=0)

client = LinodeClient('{}'.format(LINODE_PAT))

def _get_fabric_client(host):
    private_key = paramiko.rsakey.RSAKey.from_private_key_file(filename="/root/.ssh/id_rsa")
    return Connection(host, "root", connect_kwargs={
        "pkey": private_key,
        },
    )

def _init_linode_instance():

    f = open("/root/.ssh/id_rsa.pub", "r")
    public_key = f.read().rstrip('\n')
    f.close()

    # Nanode for safety, while developing
    type_id = "g6-nanode-1"
    # type_id = "g6-dedicated-8"
    # curl https://api.linode.com/v4/linode/types | jq '."data"[] | ."label"'

    region_id = "eu-west"
    image = "linode/ubuntu18.04"

    linode, password = client.linode.instance_create(type_id, region_id,
                            image=image, authorized_keys=public_key)
    return linode

def _get_all_ips(linodes):

    ips = []
    if len(linodes) == 0:
        raise RuntimeError("No servers running, try creating one first")
    for linode in linodes:
        print(linode.ipv4[0])
        ips.append(linode.ipv4[0])
    return ips

def _check_server_status(linodes, host):
    if len(linodes) == 0:
        raise RuntimeError("No servers running, try creating one first")

    for linode in linodes:
        if (linode.ipv4[0] == host):
            print(linode.status)
            return linode.status
    raise RuntimeError("Could not find server with this ip {}".format(host))

def _delete_all_servers(linodes):

    if len(linodes) == 0:
        raise RuntimeError("No linodes to delete")
    else:
        for linode in linodes:
            print("delete: ", linode.label)
            linode.delete()
        return "deleted all linodes"

def _delete_one_server(linodes, host):

    message = "Linode {} could not be found".format(host)

    if len(linodes) == 0:
        raise RuntimeError("No linodes to delete")
    else:
        for linode in linodes:
            if linode.ipv4[0] == host:
                print("delete: ", linode.label)
                linode.delete()
                return "deleted {}".format(linode.ipv4[0])

    raise RuntimeError("Could not find server with this ip {}".format(host))

def _upload_files(c, folder_path, files):
    try:
        for filename in files:
            print('Upload: {}/{}'.format(folder_path, filename))
            result = c.put('{}/{}'.format(folder_path, filename))
            # print("Uploaded {0.local} to {0.remote}".format(result))
    except Exception as e:
        RuntimeError("Could not upload install scripts to server")

def _check_exit_string(result):
    if result.exited != 0:
        return False
    return True

def _run_scripts(c):
    c.run('./install.sh')
    c.run('reboot', warn=True)

def _check_max_linode_instances(linodes, max):
    if len(linodes) >= int(max):
        raise RuntimeError("max server number of {} reached".format(MAX_LINODES))


def _read_config_file(result, lookup):
    for line in result.stdout.split('\n'):
        key, value = line.split('=')
        if key == lookup:
            return value


@http_basic_auth_login_required
@rpc_method
def create_server():
    """
    Create a py_patcher server on Linode.
    """

    linodes = client.linode.instances()
    _check_max_linode_instances(linodes, MAX_LINODES)
    linode = _init_linode_instance()

    if not linode:
        raise RuntimeError("Could not create server")

    return linode.ipv4[0]


@http_basic_auth_login_required
@rpc_method
def upload_scripts(host):
    # Change this to genuine file and pass in ENV vars or strings from NAW db entry

    scripts_path = '{}/scripts'.format(SERVER_SCRIPTS_PATH)
    templates_path = '{}/templates'.format(SERVER_SCRIPTS_PATH)

    scripts = os.listdir(scripts_path)
    templates = os.listdir(templates_path)

    if os.path.isfile('{}/darkice.cfg'.format(SERVER_SCRIPTS_PATH)):
        print ("Darkice config found")
    else:
        raise RuntimeError("Please create custom darkice config file")

    c = _get_fabric_client(host)

    _upload_files(c, scripts_path, scripts)
    _upload_files(c, templates_path, templates)
    c.put('{}/darkice.cfg'.format(templates_path))

    _run_scripts(c)

    return "successfully uploaded and installed scripts to {}".format(host)


@http_basic_auth_login_required
@rpc_method
def fetch_all_servers():
    """
    Fetch all linode server instances
    """
    # Right now this just returns the first linode as there should only be one
    linodes = client.linode.instances()
    if len(linodes) == 0:
        RuntimeError("No servers created yet")
    ips = _get_all_ips(linodes)
    return ips[0]


@http_basic_auth_login_required
@rpc_method
def delete_one_server(host):
    """
    Delete all linode server instances
    """
    linodes = client.linode.instances()
    message = _delete_one_server(linodes, host)
    return message


@http_basic_auth_login_required
@rpc_method
def delete_all_servers():
    """
    Delete all linode server instances
    """
    linodes = client.linode.instances()
    message = _delete_all_servers(linodes)
    return message


@http_basic_auth_login_required
@rpc_method
def get_server_status(host):
    """
    Get the status of our linode server.
    """

    linodes = client.linode.instances()
    status = _check_server_status(linodes, host)
    return status

@http_basic_auth_login_required
@rpc_method
def get_fpp(host):
    """
    Fetch the current JACK fpp (frames per period) value from a py_patcher server.
    :return: String
    """
    c = _get_fabric_client(host)
    try:
        result = c.run('cat /etc/jacktrip_pypatcher/jackd.conf')
    except Exception:
        raise RuntimeError("Could not get FPP value, py_patcher may not be installed")

    value = _read_config_file(result, "FPP")

    return value


@http_basic_auth_login_required
@rpc_method
def get_q(host):
    """
    Fetch the current JackTrip q (buffer) value from a py_patcher server.
    :return: String
    """
    print(host)
    c = _get_fabric_client(host)

    try:
        result = c.run('cat /etc/jacktrip_pypatcher/jacktrip.conf')
    except Exception:
        raise RuntimeError("Could not get Q value, py_patcher may not be installed")

    value = _read_config_file(result, "Q")

    return value

@http_basic_auth_login_required
@rpc_method
def set_fpp(host, fpp_value):
    """
    Set the JACK fpp (frames per period) value on a py_patcher server.
    """
    if type(fpp_value) != int:
        raise TypeError("not a number")

    result = _get_fabric_client(host).run('echo "FPP=%s" > /etc/jacktrip_pypatcher/jackd.conf' % (fpp_value))
    return result.exited


@http_basic_auth_login_required
@rpc_method
def set_q(host, q_value):
    """
    Set the JackTrip q (buffer) value on a py_patcher server.
    """
    if type(q_value) != int and q_value != "auto":
        raise TypeError("not a valid q value")

    result = _get_fabric_client(host).run('echo "Q=%s" > /etc/jacktrip_pypatcher/jacktrip.conf' % (q_value))

    return result.exited


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

