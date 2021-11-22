import subprocess


def ldap_add(file, host, bind_dn, bind_password, port=None, continuous=False):
    args = ['ldapadd', '-f', file, '-h', host, '-D', bind_dn, '-w', bind_password]
    if port:
        args += ['-p', port]
    if continuous:
        args.append('-c')
    process = subprocess.run(args, capture_output=True)
    if continuous and process.returncode == 68:
        return process

    process.check_returncode()
    return process


def ldap_delete(dn, host, bind_dn, bind_password, port=None, continuous=False, recursive=False):
    args = ['ldapdelete', dn, '-h', host, '-D', bind_dn, '-w', bind_password]
    if port:
        args += ['-p', port]
    if continuous:
        args.append('-c')
    if recursive:
        args.append('-r')

    process = subprocess.run(args, capture_output=True)
    if continuous and process.returncode == 32:
        return process
    process.check_returncode()
    return process
