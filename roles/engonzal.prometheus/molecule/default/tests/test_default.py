import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_hosts_file(host):
    f = host.file('/etc/hosts')

    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_prometheus_running_and_enabled(host):
    prom = host.service("prometheus")
    assert prom.is_running
    assert prom.is_enabled
    assert host.socket("tcp://0.0.0.0:9090").is_listening
