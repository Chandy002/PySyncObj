benchmark_tps = []
benchmark_latencies = []

with open('bench_op.txt') as op:
    op_list = op.readlines()
    singlerun_tp = []
    singlerun_latency = []
    for line in op_list:
        if line.startswith('finished'):
            continue
        if line.startswith('*****'):
            benchmark_tps.append(sum(singlerun_tp)/len(singlerun_tp))
            benchmark_latencies.append(sum(singlerun_latency)/len(singlerun_latency))
            singlerun_tp = []
            singlerun_latency = []
        line = line.split(":")
        if line[0] == 'THROUGHPUT':
            singlerun_tp.append(float(line[1]))
        elif line[0] == 'AVG LATENCY':
            singlerun_latency.append(float(line[1]))

# plot the throughput vs latency using matplotlib
import sys
from matplotlib import pyplot as plt

file_name = sys.argv[1]

plt.plot(benchmark_tps, benchmark_latencies)
plt.xlabel('Throughput (ops/sec)')
plt.ylabel('Latency (ms)')
plt.title('Baseline Performance')
plt.savefig(file_name + '.png')