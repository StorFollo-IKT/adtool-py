import logging

import slapd

process = slapd.Slapd(
    host='localhost',
    root_cn='admin',
    root_pw='test',
    port=389,
    log_level=logging.INFO,
    suffix='DC=example,DC=com'
)


def failsafe_add(file):
    with open(file) as fp:
        data = fp.read()
    try:
        process.ldapadd(data, ['-c'])
    except RuntimeError as e:
        if 'got 68' not in str(e):
            raise e


print(process.ldapwhoami().stdout.decode("utf-8"))

failsafe_add('test_data/ou_structure.ldif')
failsafe_add('test_data/users.ldif')
failsafe_add('test_data/groups.ldif')
