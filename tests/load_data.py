import logging
import os.path
from time import sleep

import slapd

process = slapd.Slapd(
    host='localhost',
    root_cn='admin',
    root_pw='test',
    port=389,
    log_level=logging.INFO,
    suffix='DC=example,DC=com',
    # debug=True,
)

process.default_ldap_uri = process.ldap_uri
process.cli_sasl_external = False


def failsafe_add(file):
    file = os.path.join(os.path.dirname(__file__), file)
    with open(file) as fp:
        data = fp.read()
    try:
        process.ldapadd(data, ['-c'])
    except RuntimeError as e:
        if 'got 68' not in str(e):
            raise e


waited = 0
wait_limit = 15

while waited < wait_limit:
    try:
        print(process.ldapwhoami().stdout.decode("utf-8"))
    except RuntimeError as e:
        sleep(1)
        waited += 1
        print('Waited %d/%d second(s) for slapd to start' % (waited, wait_limit))

failsafe_add('test_data/ou_structure.ldif')
failsafe_add('test_data/users.ldif')
failsafe_add('test_data/groups.ldif')
