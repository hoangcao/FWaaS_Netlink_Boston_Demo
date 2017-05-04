# test_performance.py

import neutronclient.v2_0.client as qclient
import keystoneclient.v2_0.client as authclient

from credentials import get_neutron_creds
from credentials import get_keystone_creds
from create_topology import create_topology

import time
import subprocess

# Get credentials
creds = get_neutron_creds()
neutron = qclient.Client(**creds)

kcreds = get_keystone_creds()
keystone = authclient.Client(**kcreds)

project_id = keystone.project_id

# Constant
START_RULE = 40000


def get_router(neutron, project_id):
    params = {"project_id": project_id,
              "description": "FWaaS-Netlink test performance"}
    routers = neutron.list_routers(**params)
    return routers

# Get router for applying firewall
try:
    routers = get_router(neutron, project_id)
    router_id = routers['routers'][0]['id']
except IndexError:
    router = create_topology(neutron, project_id)
    router_id = router['router']['id']

namespace = 'qrouter-%s' % router_id
# Create conntrack entries
# We use conntrack-tools to create conntrack entries


def create_conntrack_entries(namespace, number):
    if namespace is None:
        for sport in range(START_RULE, START_RULE + number):
            subprocess.call(['sudo', 'conntrack', '-I', '-p', 'tcp',
                             '-s', '1.1.1.1', '-d', '2.2.2.2',
                             '--sport', str(sport), '--dport', '1520',
                             '--state', 'ESTABLISHED',
                             '--timeout', '3600'])
    else:
        for sport in range(START_RULE, START_RULE + number):
            subprocess.call(['sudo', 'ip', 'netns', 'exec', namespace,
                             'conntrack', '-I', '-p', 'tcp',
                             '-s', '1.1.1.1', '-d', '2.2.2.2',
                             '--sport', str(sport), '--dport', '1520',
                             '--state', 'ESTABLISHED',
                             '--timeout', '3600'])

cases = [500]

# Listing the firewall rules
fr_ids = []
frls = neutron.list_firewall_rules()['firewall_rules']
frls = sorted(frls, key=lambda k: k['source_port'])

for case in cases:
    # Call to tcp_client to create conntrack entries
    # subprocess.call(['python', '/home/stack/tcp_client.py', str(case)])
    print case
    # Append fr_ids to update with firewall-policy
    for i in range(case):
        fr_ids.append(frls[i]['id'])

    # Create a firewall policy with all rules
    body = {'firewall_policy': {'firewall_rules': fr_ids,
                                'name': 'fp'}}
    fp = neutron.create_firewall_policy(body)
    fp_id = fp['firewall_policy']['id']

    # Create a firewall with the firewall policy above
    body = {'firewall': {'name': 'fw',
                         'admin_state_up': True,
                         'firewall_policy_id': fp_id,
                         'router_ids': [router_id]}}

    fw = neutron.create_firewall(body)
