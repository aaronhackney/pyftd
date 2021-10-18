from pyftd import FTDClient
from os import environ


def main(ftd_client, dhcp_server, dhcp_server_interface, dhcp_relay_interfaces):

    # Create DHCP Server network object (If this object already exists, it's ok, this will get skipped)
    dhcp_server_obj = ftd_client.create_network_object(dhcp_server)

    # Get interface details
    if ftd_client.get_physical_interface_list(filter=f"name:{dhcp_server_interface}"):
        dhcp_server_interface_obj = ftd_client.get_physical_interface_list(filter=f"name:{dhcp_server_interface}")[0]


def get_interface(device_int):
    if device_int == "physicalinterface":
        if ftd_client.get_physical_interface_list(filter=f"name:{dhcp_server_interface}"):
            return ftd_client.get_physical_interface_list(filter=f"name:{dhcp_server_interface}")[0]
    elif device_int == "subinterface":
        pass
    # todo deal with vlan interfaces


if "__name__" == "__main__":
    # Get ftd ip, username, and password from the env variable
    #  e.g. in bash:
    #   export FTDIP="172.30.4.28"
    #   export FTDUSER="admin"
    #   export FTDPASS="P@$$w0rd1!"

    # only set the env var "export VERIFY=True" if you want to enable TLS cert checking (Good practice but requires valid TLS cert)
    verify = True if environ.get("VERIFY") else False
    ftd_client = FTDClient(environ.get("FTDIP"), environ.get("FTDUSER"), environ.get("FTDPASS"), verify=verify)

    dhcp_server = {
        "name": "dhcp_server",
        "description": "DHCP Server Object",
        "subType": "HOST",
        "value": "192.168.3.50",
        "type": "networkobject",
    }

    # interface behind which the dhcp server resides
    dhcp_server_interface = {"name": "inside", "type": "physicalinterface"}

    # dhcp_server_interface = {"name": "inside", "type": "subinterface", parent_interface: "Ethernet1/5"}
    # interfaces where we want to enable dhcp-relay
    # valid interface types are subinterface, vlaninterface, and physicalinterface
    dhcp_relay_interfaces = [
        {"name": "inside", "type": "physicalinterface"},
    ]

    main(ftd_client, dhcp_server, dhcp_server_interface, dhcp_relay_interfaces)
