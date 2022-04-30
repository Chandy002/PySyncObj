#!/usr/bin/env xonsh

import json

def cpu_slow(slow_server_config, slow_ip, slow_pids, slowness):
    period=1000000
    quota = int(period * slowness * 0.01)
    
    sudo sh -c f'sudo mkdir /sys/fs/cgroup/cpu/db'
    sudo sh -c f'sudo echo {quota} > /sys/fs/cgroup/cpu/db/cpu.cfs_quota_us'
    sudo sh -c f'sudo echo {period} > /sys/fs/cgroup/cpu/db/cpu.cfs_period_us'
    
    for slow_pid in slow_pids.split():
        sudo sh -c f'sudo echo {slow_pid} > /sys/fs/cgroup/cpu/db/cgroup.procs'

def memory_contention(slow_server_config, slow_ip, slow_pids, slowness):    
    sudo sh -c f'sudo mkdir /sys/fs/cgroup/memory/db'
    sudo sh -c f'sudo echo {slowness} > /sys/fs/cgroup/memory/db/memory.limit_in_bytes   # 5MB'
    
    for slow_pid in slow_pids.split():
        sudo sh -c f'sudo echo {slow_pid} > /sys/fs/cgroup/memory/db/cgroup.procs'

def kill_process(ip, pids):
    for pid in pids.split():
        sudo kill -9 @(pid)

slow_vs_num = {1: cpu_slow,
               2: memory_contention}

def fault_inject(exp, server_config, pids, slowness, snooze=0):
    sleep @(snooze)
    ip = server_config["ip"]
    if exp == "kill":
        kill_process(ip, pids)
    elif exp == "noslow":
        pass
    else:
        slow_vs_num[int(exp)](server_config, ip, pids, slowness)

if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--exp", type=str, default="noslow")
    parser.add_argument("--server_configs", type=str, default="")
    parser.add_argument("--pids", type=str, default="")
    parser.add_argument("--snooze", type=int, default=0)
    parser.add_argument("--slowness", type=int, default=0)
    args = parser.parse_args()

    server_configs = json.loads(args.server_configs)
    pids = json.loads(args.pids)
    slowness = args.slowness
    
    fault_inject(args.exp, server_configs, pids, slowness, args.snooze)