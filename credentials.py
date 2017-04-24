# credentials.py

import os


def get_keystone_creds():
    d = {}
    d['username'] = os.environ['OS_USERNAME'] or "admin"
    d['password'] = os.environ['OS_PASSWORD'] or "abc123"
    d['auth_url'] = os.environ['OS_AUTH_URL'] or \
                    "http://10.164.180.97/identity_admin/v2.0"
    d['tenant_name'] = os.environ['OS_TENANT_NAME'] or "admin"
    return d


def get_neutron_creds():
    d = {}
    d['username'] = os.environ['OS_USERNAME'] or "admin"
    d['password'] = os.environ['OS_PASSWORD'] or "abc123"
    d['auth_url'] = os.environ['OS_AUTH_URL'] or \
                    "http://10.164.180.97/identity_admin/v2.0"
    d['tenant_name'] = os.environ['OS_TENANT_NAME'] or "admin"
    # Neutron service url
    d['endpoint_url'] = 'http://10.164.180.97:9696'
    return d

