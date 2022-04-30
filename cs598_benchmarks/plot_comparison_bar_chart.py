from matplotlib import pyplot as plt
import sys

title = sys.argv[1]
keys = ['noslow', 'kill', 'cpu_slow', 'memory_contention']
colors = ['red', 'green', 'blue', 'yellow']
data = []

with open(sys.argv[2]) as f:
    lines = f.readlines()
    for line in lines:
        if ':' in line:
            data.append(int(line.split(':')[1]))

plt.bar(x= keys, height = data, color=colors)
# plt.legend()
plt.xlabel('Fault Type')
plt.ylabel('Throughput (ops/sec)')
plt.title(title)
# plt.show()
plt.savefig(sys.argv[3] + '.png')