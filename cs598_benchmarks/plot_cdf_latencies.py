import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import json

def plot_cdf(directory):
    colors = ['#ffc406', 'green', 'blue', 'red']
    i = 0
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r') as f:
            lines = f.readlines()
            latencies = []
            for line in lines:
                toks = line.strip().split(':')
                if toks[0] == 'DELAYS':
                    latencies += json.loads(toks[1].strip())

            data = np.sort(np.array(latencies))
            bins=np.append(data, data[-1]+1)
            counts, bin_edges = np.histogram(latencies, bins=bins, density=False)
            counts=counts.astype(float)/len(latencies)
            cdf = np.cumsum(counts)
            plt.plot(bin_edges[0:-1], cdf, linestyle='--', color=colors[i], label=filename.split('.')[0])
            plt.ylim((0,1))
            i += 1

    plt.legend()
    plt.ylabel('CDF')
    plt.xlabel('Latency (s)')
    plt.title('Follower Latency Vs. CDF')   

    plot_margin = 0.1
    x0, x1, y0, y1 = plt.axis()
    plt.axis((x0 ,
            x1,
            y0 - plot_margin,
            y1 + plot_margin))

    plt.savefig(sys.argv[2] + '.png')

if __name__ == '__main__':
    dir = sys.argv[1]
    plot_cdf(dir)