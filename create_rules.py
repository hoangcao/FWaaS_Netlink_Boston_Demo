# create_rules.py
'''
create firewall rules with different source port
Input:
    START_RULE: start number of source port
    END_RULE: end number of source port
'''


import sys

import neutronclient.v2_0.client as qclient
from credentials import get_neutron_creds
creds = get_neutron_creds()
neutron = qclient.Client(**creds)

START_RULE = int(sys.argv[1])
END_RULE = int(sys.argv[2])

for source_port in range(START_RULE, END_RULE):
    if source_port % 100 == 0:
        print source_port
    body = {'firewall_rule': {
                    'action': 'allow', 'enabled': True, 'protocol': 'tcp',
                    'source_port': str(source_port), 'destination_port': '1520', }}
    neutron.create_firewall_rule(body)
