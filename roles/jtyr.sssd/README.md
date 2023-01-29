sssd
====

Role which helps to install sssd - System Security Services Daemon.

The configuration of the role is done in such way that it should not be necessary
to change the role for any kind of configuration. All can be done either by
changing role parameters or by declaring completely new configuration as a
variable. That makes this role absolutely universal. See the examples below for
more details.

Please report any issues or send PR.


Example
-------

```
---

# Default usage
- hosts: myhost1
  roles:
    - sssd

# Example of how to configure sssd
- hosts: myhost2
  vars:
    # Simply overwrite this variable with new configuration
    sssd_config:
        ...
        ...
  roles:
    - sssd
```


Role variables
--------------

List of variables used by the role:

```
# Package to be installed (you can force a specific version here)
sssd_pkg: sssd

# Default sssd config (you probably want to overwrite this)
sssd_config:
  sssd:
    domains: LOCAL
    services: nss
    config_file_version: 2
  nss:
    filter_groups: root
    filter_users: root
  'domain/LOCAL':
    id_provider: local
    auth_provider: local
    access_provider: permit
```


Dependencies
------------

- [`config_encoder_filters`](https://github.com/jtyr/ansible-config_encoder_filters)


License
-------

MIT


Author
------

Jiri Tyr
