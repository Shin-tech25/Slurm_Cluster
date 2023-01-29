# prometheus

Installs and configures 

[![Build Status](https://travis-ci.org/engonzal/ansible_role_prometheus.svg?branch=master)](https://travis-ci.org/engonzal/ansible_role_prometheus)

## Todo

* Add tasks to configure Prometheus Blackbox (web http monitoring) as an option.

## Requirements

Note that this role requires root.  Ensure ```become: yes``` is set at the top level of your playbook or invoke the role in your playbook like:

```yaml
- hosts: all
  roles:
    - role: engonzal.prometheus
      become: yes
```

## Role Variables

Available variable with examples are below:

```yaml
prom_version: "2.12.0"
```

Use ```prom_version``` to specify a version of Prometheus to install.  Checkout <https://github.com/prometheus/prometheus/releases> to see the latest releases.

```yaml
prom_user: "prometheus"
prom_group: "{{ prom_user }}"
```

You can specify the user to run prometheus as, by default it will run as the user and group "prometheus".  If the user/group do not exist they will be created.

```yaml
prom_dir_base: "/app"
prom_dir_main: "{{ prom_dir_base }}/prometheus"
prom_dir_config: "{{ prom_dir_main }}/config"
prom_dir_data: "{{ prom_dir_main }}/data"
prom_dir_bin: "{{ prom_dir_main }}/bin"
```

You can set custom locations for the app, config, and data directories.  By default everything will be installed at /app

```yaml
prom_web_uri: "http://prometheus.example.com:9090"
```

If you will be adding a proxy redirect you can specify the URL for that.  It will default to the hosts FQDN (using the ```ansible_fqdn```).

```yaml
prom_groups:
  local: 
    - localhost
  webservers:
    - we.example.com
  admin:
    - admin.example.com
```

By default this role will use all the groups from the inventory file you use.  To customize this you can change the ```prom_groups``` variable, please note that you must format it like the example above (dictionary with group items, each group needs to have a list).  Looking to make this easier to use in the future, but for now it does the job.

Also note that this will use the domain of the target prometheus server (using the ```ansible_domain``` variable set during setup).

## Example Playbook

### Simple Example (defaults)

```yaml
- hosts: servers
  roles:
      - { role: engonzal.prometheus }
```

## License

BSD

## Author Information

This role was created in 2019 by Noe Gonzalez (<http://engonzal.com> and <https://buildahomelab.com>)
