# create_topology.py


def get_external_network(neutron, project_id):
    params = {
        "project_id": project_id,
        "router:external": True}

    ex_net = neutron.list_networks(**params)

    return ex_net


def create_internal_network(neutron, project_id):
    params = {
        "network": {
        "project_id": project_id,
        "name": "net1",
        "description": "FWaaS-Netlink test performance", }}

    int_net = neutron.create_network(params)

    return int_net


def create_internal_subnet(neutron, project_id, network):
    params = {
        "subnet": {
        "project_id": project_id,
        "name": "subnet1",
        "description": "FWaaS-Netlink test performance",
        "network_id": network['network']['id'],
        "ip_version": 4,
        'cidr': '10.0.0.0/24', }}
    sub_net = neutron.create_subnet(params)

    return sub_net


def create_router(neutron, project_id, ex_network):
    params = {
        "router": {
            "project_id": project_id,
            "name": "routera",
            "description": "FWaaS-Netlink test performance",
            "external_gateway_info": {
                "network_id": ex_network
            },
            "admin_state_up": True,

        }
    }
    router = neutron.create_router(params)
    return router


def create_topology(neutron, project_id):
    ext_net = get_external_network(neutron, project_id)
    try:
        router = create_router(neutron, project_id, ext_net['networks'][0]['id'])
    except KeyError:
        pass

    return router
