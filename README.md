# Slurm Cluster DBD Node

[galaxyproject/ansible-slurm](https://github.com/galaxyproject/ansible-slurm) を参考にして1 x 仮想マスターノード、2 x 仮想計算ノードのSlurm Clusterを構築してみました。

また、Slurmdbdで作成するデータベースは、[bertvv/ansible-role-mariadb](https://github.com/bertvv/ansible-role-mariadb)を用いて作成しました。

## 使ったrole（一部コード修正あり）

[Ansible Galaxy](https://galaxy.ansible.com/)には、再利用性の高いAnsible コードが有志によってアップロードされています。今回は以下のコードを使わせて頂きました。

- [Ansible-Galaxy bertvv.hosts](https://galaxy.ansible.com/bertvv/hosts)
- [Ansible-Galaxy bertvv.mariadb](https://galaxy.ansible.com/bertvv/mariadb)
- [Ansible-Galaxy galaxyproject.slurm](https://galaxy.ansible.com/galaxyproject/slurm)
- [Ansible-Galaxy geerlingguy.nfs](https://galaxy.ansible.com/geerlingguy/nfs)
- [Ansible-Galaxy ome.nfs_mount](https://galaxy.ansible.com/ome/nfs_mount)
- [Ansible-Galaxy geerlingguy.ntp](https://galaxy.ansible.com/geerlingguy/ntp)
- [Ansible-Galaxy jtyr.sssd](https://galaxy.ansible.com/jtyr/sssd)
- [Ansible-Galaxy jtyr.config_encoder_filters](https://galaxy.ansible.com/jtyr/config_encoder_filters)


## 環境

ホストマシンにVagrant, VirtualBox, Ansibleがインストールされている必要があります。

![Slurm_Cluster_dbdnode](./Slurm_Cluster_dbdnode.png)

```
$ vagrant --version
Vagrant 2.3.3
$ ansible --version
ansible [core 2.14.0]
$ python --version
Python 3.11.0
```

## 仮想マシンの作成

以下のコマンドで仮想マシンを作成出来ます。
```
$ vagrant up
$ ansible-playbook playbook.yml
```

必要に応じて、`Vagrantfile`や`inventory`のIPアドレス、ネットワーク設定などを変更して下さい。

## 変数
タスク変数は`vars`ディレクトリ以下に定義されています。これは、`roles`以下のデフォルトの変数を上書きする形で`playbook.yml`から読み込んでいます。

```
vars/
├── hosts.yml   # roles/bertvv.hostsのrole変数を上書き
├── mariadb.yml # roles/bertvv.mariadbのrole変数を上書き
└── slurm.yml   # roles/galaxyproject.slurmのrole変数を上書き
```

### Example

``` YAML

# vars/hosts.yml

hosts_entries:
  - ip: 192.168.56.44
    name: slurmmaster slurmmaster.local
  - ip: 192.168.56.45
    name: slurmbatch1 slurmbatch1.local
  - ip: 192.168.56.46
    name: slurmbatch2 slurmbatch2.local

# /etc/hosts.ymlに記載される。
# 192.168.56.44 slurmmaster slurmmaster.local
# 192.168.56.45 slurmbatch1 slurmbatch1.local
# 192.168.56.46 slurmbatch2 slurmbatch2.local

# vars/mariadb.yml

mariadb_mirror: 'mirror.mariadb.org/yum'
mariadb_bind_address: '0.0.0.0' # 全てのインターフェースからアクセス許可
mariadb_root_password: 'atOrryag&'  # rootパスワード
mariadb_server_cnf:
  general-log:
  general-log-file: 'queries.log'
  slow-query-log:
  slow-query-log-file: 'mariadb-slow.log'
  long-query-time: '5.0'
mariadb_custom_cnf:
  mariadb:
    autoset_open_files_limit:
    max-connections: '20'
  mysqld:
    language: /usr/share/mysql/japanese
    innodb_buffer_pool_size: '4096M'
    innodb_log_file_size: '64M'
    innodb_lock_wait_timeout: '900'
mariadb_configure_swappiness: true
mariadb_swappiness: '10'
mariadb_databases:
  - name: slurm_acct_db # Slurmdbd用のDB
    # init_script: ../molecule/common/init.sql
mariadb_users:
  - name: slurm # slurm dbユーザ
    password: 'SLURM'   # slurm dbユーザ用パスワード（平文）
    priv: 'slurm_acct_db.*:ALL'
    host: '%'   # Allow access from all hosts.

# vars/slurm.yml

# Slurmの各種設定は以下
slurm_config:
  AccountingStorageType: "accounting_storage/none"
  ClusterName: cluster
  SlurmctldHost: "slurmmaster.local"
  SlurmctldLogFile: "/var/log/slurm/slurmctld.log"
  SlurmctldPidFile: "/var/run/slurmctld.pid"
  SlurmdLogFile: "/var/log/slurm/slurmd.log"
  SlurmdPidFile: "/var/run/slurmd.pid"
  SlurmdSpoolDir: "/var/spool/slurmd"
  StateSaveLocation: "/var/spool/slurmctld"
slurm_create_user: yes
slurm_user:
  comment: "Slurm Workload Manager"
  gid: 888
  group: slurm
  home: "/var/lib/slurm"
  name: slurm
  shell: "/usr/sbin/nologin"
  uid: 888
# /etc/slurm/slurm.confのパーティション設定、ノード名など
slurm_partitions:
  - name: debug
    Default: YES
    MaxTime: UNLIMITED
    Nodes: "slurmbatch1.local,slurmbatch2.local"
slurm_nodes:
  - name: "slurmbatch1.local"
  - name: "slurmbatch2.local"

```

## メリット

Slurmの設定やMUNGEとの連携などをよろしくやってくれます。Slurmdbdとの連携、`slurm_acct_gather_config`,`slurm_cgroup_config`,`slurm_gres_config`などのパラメータも同様にハッシュ形式で指定できます。

`/etc/hosts`や`/etc/slurm/slurm.conf`等設定ファイルは共通に使わなければならない制約があることや、計算ノードをスケールさせたい際にPlaybookとして配れれば便利。

`hosts.yml`では、`/etc/hosts`に記載されるホスト情報を設定します。

`mariadb.yml`では、SlurmdbdサーバのMariaDBのパラメータを設定します。

`slurm.yml`では、Slurmの各種設定を行うことが出来ます。

## Slurmdbd 設定


以下のサイト等を参考にした。
- [slurm/accounting](https://web.chaperone.jp/w/index.php?slurm/accounting)


## 参考

- [Slurm Workload Manager Documentation](https://slurm.schedmd.com/documentation.html)
- [galaxyproject/ansible-slurm](https://github.com/galaxyproject/ansible-slurm)
- [bertvv/ansible-role-mariadb](https://github.com/bertvv/ansible-role-mariadb)