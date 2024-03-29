import io
import os
import sys
import ansible_runner
import paramiko
from environs import Env
from fabric import Connection
from linode_api4 import LinodeClient
from modernrpc.auth.basic import http_basic_auth_login_required
from modernrpc.core import rpc_method

# Load environment variables
env = Env()
env.read_env()

LINODE_PAT = env("LINODE_PAT", default="")
MAX_LINODES = env("MAX_LINODES", default=0)
PRIVATE_KEY = env("PRIVATE_KEY", default="")
LOUNGE_MUSIC_URL = env("LOUNGE_MUSIC_URL", default="")
ICECAST_SERVER_URL = env("ICECAST_SERVER_URL", default="")
ICECAST_PORT = env("ICECAST_PORT", default="")
ICECAST_MOUNT = env("ICECAST_MOUNT", default="")
ICECAST_PASSWORD = env("ICECAST_PASSWORD", default="")


def _client():
    return LinodeClient("{}".format(LINODE_PAT))
    

def _setup_server_ip():
    if LINODE_PAT == "":
        print("An invalid Linode PAT string was provided, not attempting server communication.")
        return

    # Check if there are any already running linode instances and if so fetch the ip
    # We can only create one instance, so we just take the first ip present
    linodes = _client().linode.instances()
    f = open("/server/pypatcher-ansible/inventory", "wt")
    if len(linodes) > 0:
        f.write(linodes[0].ipv4[0])
    else:
        f.write("")        
    f.close()


def _setup_keys():
    if PRIVATE_KEY == "":
        print("An invalid PrivateKey string was provided, not initializing keys")
        return
    
    # Create .ssh folder in root if it doesn't exist
    try:
        os.mkdir("/root/.ssh")
    except FileExistsError:
        pass

    # Write private key to file
    _private_key().write_private_key_file("/root/.ssh/id_rsa")
    # Write public key to file
    f = open("/root/.ssh/id_rsa.pub", "wt")
    f.write(_public_key())
    f.close()


def _private_key():
    # RSA keypair from PRIVATE_KEY string
    return paramiko.RSAKey.from_private_key(io.StringIO(PRIVATE_KEY))


def _public_key():
    # Retrieve the public key of the keypair
    return "ssh-rsa " + _private_key().get_base64()


def _get_fabric_client(host):
    # Return a fabric connection
    return Connection(host, "root", connect_kwargs={"pkey": _private_key(),},)


def _init_linode_instance():
    # Nanode for safety, while developing
    type_id = "g6-nanode-1"
    region_id = "eu-west"
    image = "linode/ubuntu20.04"

    linode, password = _client().linode.instance_create(
        type_id, region_id, image=image, authorized_keys=_public_key()
    )
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
        if linode.ipv4[0] == host:
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
    if len(linodes) == 0:
        raise RuntimeError("No linodes to delete")
    else:
        for linode in linodes:
            if linode.ipv4[0] == host:
                print("delete: ", linode.label)
                linode.delete()
                return "deleted {}".format(linode.ipv4[0])

    raise RuntimeError("Could not find server with this ip {}".format(host))


def _check_max_linode_instances(linodes, max):
    if len(linodes) >= int(max):
        raise RuntimeError("max server number of {} reached".format(MAX_LINODES))


def _read_config_file(result, lookup):
    for line in result.stdout.split("\n"):
        key, value = line.split("=")
        if key == lookup:
            return value


@http_basic_auth_login_required
@rpc_method
def create_server():
    """
    Create a py_patcher server on Linode.
    """

    linodes = _client().linode.instances()
    _check_max_linode_instances(linodes, MAX_LINODES)
    linode = _init_linode_instance()

    if not linode:
        raise RuntimeError("Could not create server")

    f = open("/server/pypatcher-ansible/inventory", "wt")
    f.write(linode.ipv4[0])
    f.close()

    return linode.ipv4[0]


@http_basic_auth_login_required
@rpc_method
def setup_server():

    if not os.path.exists("/server/pypatcher-ansible/inventory"):
        raise RuntimeError("Server ip address not found (no inventroy file")

    out, err, rc = ansible_runner.run_command(
        executable_cmd="ansible-playbook",
        cmdline_args=[
            "/server/pypatcher-ansible/setup-server.yml",
            "-i",
            "/server/pypatcher-ansible/inventory",
            "--private-key",
            "/root/.ssh/id_rsa",
            "-u",
            "root",
            "--extra-vars",
            "variable_host=all",
        ],
        input_fd=sys.stdin,
        output_fd=sys.stdout,
        error_fd=sys.stderr,
    )
    print("rc: {}".format(rc))
    print("out: {}".format(out))
    print("err: {}".format(err))

    return 'rc: {} \nout: {}\nerr: {}'.format(rc, out, err)


@http_basic_auth_login_required
@rpc_method
def install_pypatcher():
    if not os.path.exists("/server/pypatcher-ansible/inventory"):
        raise RuntimeError("Server ip address not found (no inventroy file")

    # Change this to genuine file and pass in ENV vars or strings from NAW db entry
    out, err, rc = ansible_runner.run_command(
        executable_cmd="ansible-playbook",
        cmdline_args=[
            "/server/pypatcher-ansible/install-pypatcher.yml",
            "-i",
            "/server/pypatcher-ansible/inventory",
            "--private-key",
            "/root/.ssh/id_rsa",
            "-u",
            "root",
            "--extra-vars",
            '"variable_host=all lounge_music_url={} icecast_server_url={} icecast_port={} icecast_mount={} icecast_password={}"'.format(
                LOUNGE_MUSIC_URL,
                ICECAST_SERVER_URL,
                ICECAST_PORT,
                ICECAST_MOUNT,
                ICECAST_PASSWORD,
            ),
        ],
        input_fd=sys.stdin,
        output_fd=sys.stdout,
        error_fd=sys.stderr,
    )
    print("rc: {}".format(rc))
    print("out: {}".format(out))
    print("err: {}".format(err))

    return 'rc: {} \nout: {}\nerr: {}'.format(rc, out, err)


@http_basic_auth_login_required
@rpc_method
def fetch_all_servers():
    """
    Fetch all linode server instances
    """
    # Right now this just returns the first linode as there should only be one
    linodes = _client().linode.instances()
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
    linodes = _client().linode.instances()
    message = _delete_one_server(linodes, host)
    return message


@http_basic_auth_login_required
@rpc_method
def delete_all_servers():
    """
    Delete all linode server instances
    """
    linodes = _client().linode.instances()
    message = _delete_all_servers(linodes)
    return message


@http_basic_auth_login_required
@rpc_method
def get_server_status(host):
    """
    Get the status of our linode server.
    """

    linodes = _client().linode.instances()
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
        result = c.run("cat /etc/jacktrip_pypatcher/jackd.conf")
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
        result = c.run("cat /etc/jacktrip_pypatcher/jacktrip.conf")
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

    result = _get_fabric_client(host).run(
        'echo "FPP=%s" > /etc/jacktrip_pypatcher/jackd.conf' % (fpp_value)
    )
    return result.exited


@http_basic_auth_login_required
@rpc_method
def set_q(host, q_value):
    """
    Set the JackTrip q (buffer) value on a py_patcher server.
    """
    if type(q_value) != int and q_value != "auto":
        raise TypeError("not a valid q value")

    result = _get_fabric_client(host).run(
        'echo "Q=%s" > /etc/jacktrip_pypatcher/jacktrip.conf' % (q_value)
    )

    return result.exited


@http_basic_auth_login_required
@rpc_method
def restart_jacktrip(host):
    """
    Restart JackTrip on a py_patcher server.
    """
    result = _get_fabric_client(host).run("sudo systemctl restart jacktrip.service")
    return result.exited


@http_basic_auth_login_required
@rpc_method
def restart_jackd(host):
    """
    Restart JACK on a py_patcher server.
    """
    result = _get_fabric_client(host).run("sudo systemctl restart jackd.service")
    return result.exited


## Run setup commands

_setup_keys()
_setup_server_ip()
