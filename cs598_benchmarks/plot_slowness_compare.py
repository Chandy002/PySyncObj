from matplotlib import pyplot as plt
import sys
import numpy as np

bar_width = 0.1
index = np.arange(2)

## cpu_slow##
# slow_tp_5_data = [5118, 4061]
# slow_tp_10_data = [4995, 5292]
# slow_tp_20_data = [2533, 1730]
# slow_tp_50_data = [6150, 8103]
# slow_tp_70_data = [5987, 7502]
# slow_tp_80_data = [6851, 7840]
# slow_tp_baseline = [8218, 8218]

# slow_lat_5_data = [0.3536539872487386, 0.5233095089594523]
# slow_lat_10_data = [0.5165612697601318, 0.32027530670166016]
# slow_lat_20_data = [5.358139246702194, 4.387077437506782]
# slow_lat_50_data = [6.368323352601793, 3.009563684463501]
# slow_lat_70_data = [6.314730591244167, 2.757071574529012]
# slow_lat_80_data = [4.770405107074314, 2.4704702695210776]
slow_lat_baseline = []

## memory_contention##
# slow_tp_5kb_data = [5133, 5390]
# slow_tp_1mb_data = [5133, 5500]
# slow_tp_5mb_data = [5111, 5197]
# slow_tp_10mb_data = [8250, 8250]
# slow_tp_20mb_data = [8250, 8250]
# slow_tp_baseline = [8218, 8218]

slow_lat_5kb_data = [0.3309938907623291, 0.3372191588083903]
slow_lat_1mb_data = [0.3582509756088257, 0.3197591304779053]
slow_lat_5mb_data = [0.3236011266708374, 0.5328935384750366]
slow_lat_10mb_data = [1.223832580778334, 1.3199706077575684]
# slow_lat_20mb_data = [1.3546925915612116, 1.384733862347073]
slow_lat_baseline = [2.7203097343444824, 2.7203097343444824]

# fig = plt.figure()
# ax = fig.add_axes([0,1])

plt.figure(figsize=(7,5))
# slow_5 = plt.bar(index, slow_tp_5_data, 
#                 width=bar_width, label="5%", color='red')

# slow_10 = plt.bar(index + bar_width, slow_tp_10_data,
#                 width=bar_width, label="10%", color='green')

slow_20 = plt.bar(index - 2*bar_width, slow_lat_5kb_data,
                width=bar_width, label="5 KB", color='red')

slow_50 = plt.bar(index - bar_width, slow_lat_1mb_data,
                width=bar_width, label="1 MB", color='yellow')

slow_70 = plt.bar(index, slow_lat_5mb_data,
                width=bar_width, label="5 MB", color='orange')

slow_80 = plt.bar(index + bar_width, slow_lat_10mb_data,
                bar_width, label="10 MB", color='green')

# slow_80 = plt.bar(index + bar_width, slow_lat_20mb_data,
#                 bar_width, label="20 MB", color='cyan')

slow_baseline = plt.bar(index + 2*bar_width, slow_lat_baseline,
                bar_width, label="noslow", color='blue')

# ax.set_ylabel('Throughput (ops/sec)')
# ax.set_xlabel('Node Type')
# ax.set_xticks(index + bar_width/2)
# ax.set_xticklabels(("Leader", "Follower"))
# ax.legend()

plt.xlabel('Node Type')
plt.ylabel('P50 Latency (s)')
plt.title(sys.argv[2])
plt.xticks(index + bar_width/2, ["Leader", "Follower"])
plt.legend()

plt.savefig(sys.argv[1] + '.png')