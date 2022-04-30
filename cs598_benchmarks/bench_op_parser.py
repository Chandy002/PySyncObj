import sys
from matplotlib import pyplot as plt

benchmark_tps = []
benchmark_latencies = []
benchmark_p90_latencies = []
benchmark_p99_latencies = []
benchmark_nodes_alive = []

decline_noticed = False
tail_rounds = 0
it = None
max_tp = 0
max_tp_it = 0
singlerun_nodes_alive = 0

ip_file_name = sys.argv[1]
with open(ip_file_name + '.txt') as op:
    op_list = op.readlines()
    singlerun_tp = []
    singlerun_latency = []
    singlerun_p90_latency = []
    singlerun_p99_latency = []
    for line in op_list:
        if line.startswith('finished'):
            it = line.split(' ')[-1]
            continue
        if line.startswith('*****'):
            benchmark_tps.append(sum(singlerun_tp)/3)
            benchmark_latencies.append(sum(singlerun_latency)/len(singlerun_latency))
            benchmark_p90_latencies.append(sum(singlerun_p90_latency)/len(singlerun_p90_latency))
            benchmark_p99_latencies.append(sum(singlerun_p99_latency)/len(singlerun_p99_latency))
            benchmark_nodes_alive.append(singlerun_nodes_alive)
            
            # if tail_rounds == 2:
            #     break
            # if decline_noticed:
            #     tail_rounds += 1
            # elif len(benchmark_tps) > 2 and benchmark_tps[-1] < benchmark_tps[-2]:
            #     decline_noticed = True
            #     print("MAX THROUGHPUT:", benchmark_tps[-2], "ITERATION:", it)
            #     tail_rounds += 1

            if benchmark_tps[-1] > max_tp:
                max_tp_it = it
                max_tp = benchmark_tps[-1]
                max_tp_lat = benchmark_latencies[-1]
                max_tp_p90_lat = benchmark_p90_latencies[-1]
                max_tp_p99_lat = benchmark_p99_latencies[-1]

            singlerun_tp = []
            singlerun_latency = []
            singlerun_nodes_alive = 0

        line = line.split(":")
        if line[0] == 'THROUGHPUT':
            singlerun_nodes_alive += 1
            singlerun_tp.append(float(line[1]))
        elif line[0] == 'AVG LATENCY':
            singlerun_latency.append(float(line[1]))
        elif line[0] == 'P90 LATENCY':
            singlerun_p90_latency.append(float(line[1]))
        elif line[0] == 'P99 LATENCY':
            singlerun_p99_latency.append(float(line[1]))

# plot the throughput vs latency using matplotlib
if sys.argv[2] == 'plot':
    op_file_name = sys.argv[3]

    # plt.plot(benchmark_tps, benchmark_nodes_alive, color='green')
    plt.plot(benchmark_tps, benchmark_latencies)
    plt.xlabel('Throughput (ops/sec)')
    plt.ylabel('P50 Latency (s)')
    plt.title('Baseline Performance')
    plt.savefig(op_file_name + '.png')

print("MAX THROUGHPUT:", max_tp, "\nITERATION:", max_tp_it, "\nAVG LATENCY:", max_tp_lat, "\nP99:", max_tp_p99_lat, "\nP90:", max_tp_p90_lat)