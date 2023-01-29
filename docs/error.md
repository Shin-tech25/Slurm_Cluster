

## Error 2023.01.12

slurmbatch1 and slurmbatch2

→ An error occured.
```
[2023-01-12T05:20:15.562] error: Configured MailProg is invalid
[2023-01-12T05:20:15.562] slurmctld version 20.11.9 started on cluster cluster
[2023-01-12T05:20:15.564] No memory enforcing mechanism configured.
[2023-01-12T05:20:15.566] error: Could not open node state file /var/spool/slurmctld/node_state: No such file or directory
[2023-01-12T05:20:15.566] error: NOTE: Trying backup state save file. Information may be lost!
[2023-01-12T05:20:15.566] No node state file (/var/spool/slurmctld/node_state.old) to recover
[2023-01-12T05:20:15.566] error: Could not open job state file /var/spool/slurmctld/job_state: No such file or directory
[2023-01-12T05:20:15.566] error: NOTE: Trying backup state save file. Jobs may be lost!
[2023-01-12T05:20:15.566] No job state file (/var/spool/slurmctld/job_state.old) to recover
```

## 対応
```
sudo dnf install munge-devel
```

何かメモリエラー起こしてるっぽい？
仮想マシン多重起動のためのメモリエラー問題？？