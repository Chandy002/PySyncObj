from __future__ import print_function
import subprocess
import os
import argparse
import json

DEVNULL = open(os.devnull, 'wb')

START_PORT = 4321
MIN_RPS = 10
MAX_RPS = 40000
NUM_RUNS = 165

def singleBenchmark(server_configs, exp, exp_type, slowness, requestsPerSecond, requestSize, numNodes):
    rpsPerNode = int(requestsPerSecond / numNodes)
    processes = []
    allAddrs = []

    for i in range(numNodes):
        allAddrs.append(server_configs[i]["ip"] + ':%d' % (START_PORT + server_configs[i]["port_offset"]))

    for i in range(numNodes):
        addrs = list(allAddrs)
        selfAddr = addrs.pop(i)

        process_cmd = f"python3 testobj_latency_tp.py {rpsPerNode} {requestSize} {server_configs[i]['cpu']} {selfAddr} {' '.join(addrs)}"
        cmd = ['/bin/bash', '-c', process_cmd]
        p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        processes.append(p)

    #### code added for fault injection ####
    allLeaders = []
    server_pids = {}
    while len(allLeaders) < numNodes:
        allLeaders = []
        server_pids = {}
        for i in range(numNodes):
            leader = None
            try:
                with open('leader' + str(START_PORT + server_configs[i]["port_offset"]), 'r') as f:
                    lines = f.readlines()
                    leader = lines[0].split(' ')[1]
                    selfAddr = f'{server_configs[i]["ip"]}:{str(START_PORT + server_configs[i]["port_offset"])}'
                    t_id = int(lines[1].split(' ')[1].strip())
            except:
                pass
            if leader is not None and leader.strip() != '':
                allLeaders.append(leader.strip())
                server_pids[selfAddr.strip()] = t_id

    # Found the leader
    assert len(allLeaders) == numNodes
    # print(server_pids)

    leader_pid = server_pids[allLeaders[0]]
    for server_config in server_configs:
        if server_config["ip"] + ':%d' % (START_PORT + server_config["port_offset"]) != leader:
            followerip = server_config["ip"] + ':%d' % (START_PORT + server_config["port_offset"])
            follower_pid = server_pids[followerip]
            break
    
    # set fault pids and fault_config
    if exp_type == "follower":
        fault_replica = followerip
        fault_pids = str(follower_pid)
    elif exp_type == "leader":
        fault_replica = allLeaders[0]
        fault_pids = str(leader_pid)

    for cfg in server_configs:
        if cfg["ip"] + ':%d' % (START_PORT + cfg["port_offset"]) == fault_replica:
            fault_config = cfg
            break

    # run fault injection
    fault_process_cmd = ["xonsh", "faults/fault_inject.xsh", "--exp", f"{exp}", "--slowness", f"{slowness}", "--server_configs", f"{json.dumps(fault_config)}", "--pids", f"{json.dumps(fault_pids)}"]
    subprocess.run(fault_process_cmd, stdout=subprocess.PIPE)


    for p in processes:
        out, err = p.communicate()
        print(out.decode('utf-8'), end='')

    # remove leader files
    for i in range(numNodes):
        os.remove('leader' + str(START_PORT + server_configs[i]["port_offset"]))

    # kill deadloop processes
    get_deadloop_processes = subprocess.Popen(['pgrep', 'deadloop'], stdout=subprocess.PIPE)
    deadloop_processes = get_deadloop_processes.communicate()[0].decode('utf-8').split('\n')
    for p in deadloop_processes:
        if p != '':
            subprocess.Popen(['kill', '-9', p])

def config_parser(path):
    with open(path) as f:
        nodes = json.load(f)

    return nodes

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--iters", type=int, default=3, help="number of iterations")
    parser.add_argument("--server_configs", type=str, default="faults/server_configs.json", help="server config path")
    parser.add_argument("--exp", type=str, default="noslow", help="kill/noslow/1/2")
    parser.add_argument("--exp_type", type=str, default="follower", help="leader/follower/both")
    parser.add_argument("--slowness", type=int, default=0, help="slowness")
    opt = parser.parse_args()

    server_configs = config_parser(opt.server_configs)["servers"]
    for i in range(165, NUM_RUNS + 1, 3):
        for iter in range(1, opt.iters+1):
            singleBenchmark(server_configs, opt.exp, opt.exp_type, opt.slowness, 50*i, 10, 3)
        print('finished iteration %d' % i)
        print('*****')