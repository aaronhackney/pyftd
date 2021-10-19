from pyftd import FTDClient
from os import environ


def main(ftd_client, dhcp_server, dhcp_server_interface, dhcp_relay_interfaces):
    # Interface objects where we want to enable DHCP RELAY
    dhcp_relay_intf_objs = []

    # Create DHCP Server network object (If this object already exists, it's ok)
    dhcp_server_obj = ftd_client.get_network_object_list(filter=f"name:{dhcp_server['name']}")
    if dhcp_server_obj is None:
        dhcp_server_obj = ftd_client.create_network_object(dhcp_server)
    else:
        dhcp_server_obj = dhcp_server_obj[0]

    # Get the intf obj of the interface where the DHCP server lives
    dhcp_server_intf_obj = search_interfaces(dhcp_server_interface, ftd_client)

    # Get the intf obj of the interfaces where we want to enable DHCP RELAY
    for dhcp_relay_interface in dhcp_relay_interfaces:
        intf = search_interfaces(dhcp_relay_interface, ftd_client)
        if intf is not None:
            dhcp_relay_intf_objs.append(intf)

    updated_dhcp_relay_obj = set_dhcp_relay(dhcp_server_obj, dhcp_server_intf_obj, dhcp_relay_intf_objs, ftd_client)
    print("DHCP Servers:")
    print("--------------------------------------------------")
    for dhcp_svr in updated_dhcp_relay_obj.servers:
        print(f'{dhcp_svr["server"]["name"]} on interface {dhcp_svr["interface"]["name"]}')

    print("\nDHCP RELAY ENABLED INTERFACES:")
    print("--------------------------------------------------")
    for relay_interface in updated_dhcp_relay_obj.agents:
        print(f'{relay_interface["interface"]["name"]}')

    print("Double check your settings in the UI and don't forget to deploy")


def set_dhcp_relay(dhcp_svr_obj: dict, dhcp_svr_intf_obj: dict, dhcp_relay_intf_objs: list, ftd_client: FTDClient):
    # Get dhcp relay services object
    dhcp_relay_obj = ftd_client.get_dhcp_relay_services()[0]

    # Add the dhcp server to the dhcp relay services object
    if dhcp_relay_obj.servers is None:
        dhcp_relay_obj.servers = []

    dhcp_relay_obj.servers.append(
        {
            "server": dhcp_svr_obj,
            "interface": dhcp_svr_intf_obj,
            "type": "dhcprelayserver",
        }
    )

    # Add the interfaces to enable dhcp relay to the dhcp relay services object
    if dhcp_relay_obj.agents is None:
        dhcp_relay_obj.agents = []

    for dhcp_relay_intf_obj in dhcp_relay_intf_objs:
        dhcp_relay_obj.agents.append(
            {
                "enableIpv4Relay": True,
                "setRoute": True,
                "interface": dhcp_relay_intf_obj,
                "type": "dhcprelayagent",
            }
        )

    # Update the dhcp relay and server settings on the device
    return ftd_client.update_dhcp_relay_service(dhcp_relay_obj)


def search_interfaces(intf_name: str, ftd_client: FTDClient) -> dict:
    """Given an interface name (nameif) return the interface object
    :param intf_name: name of interface
    :param ftd_client: FTDClient pyftd client obj
    :return: dict interface object
    """
    if ftd_client.get_physical_interface_list(filter=f"name:{intf_name}"):
        return ftd_client.get_physical_interface_list(filter=f"name:{intf_name}")[0]
    elif ftd_client.get_vlan_interface_list(filter=f"name:{intf_name}"):
        return ftd_client.get_vlan_interface_list(filter=f"name:{intf_name}")[0]
    else:
        phys_intf_list = ftd_client.get_physical_interface_list()
        for intf in phys_intf_list:
            if ftd_client.get_sub_interface_list(intf.id, filter=f"name:{intf_name}"):
                return ftd_client.get_sub_interface_list(intf.id, filter=f"name:{intf_name}")[0]


if __name__ == "__main__":
    # Get ftd ip, username, and password from the env variable
    #  e.g. in bash:
    #   export FTDIP="172.30.4.28"
    #   export FTDUSER="admin"
    #   export FTDPASS="P@$$w0rd1!"
    #   export FTDPORT="8080"

    # only set the env var "export VERIFY=True" if you want to enable TLS cert checking otherwise omit (requires valid TLS cert)
    verify = True if environ.get("VERIFY") else False
    ftd_client = FTDClient(
        environ.get("FTDIP"),
        environ.get("FTDUSER"),
        environ.get("FTDPASS"),
        fdm_port=environ.get("FTDPORT"),
        verify=verify,
    )

    # TODO: move all of this to a yaml file
    dhcp_server = {
        "name": "dhcp_server",
        "description": "DHCP Server Object",
        "subType": "HOST",
        "value": "192.168.3.50",
        "type": "networkobject",
    }

    # interface behind which the dhcp server resides
    dhcp_server_interface = "management"

    # interfaces where we want to enable dhcp-relay
    dhcp_relay_interface_names = [
        "inside",
        "lab_pod_all_outside",
        "lab_pod_all_management",
        "app",
        "guest",
        "dmz",
    ]

    main(ftd_client, dhcp_server, dhcp_server_interface, dhcp_relay_interface_names)
