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
# slow_tp_baseline = [8250, 8250]

## p50 ##
# slow_lat_5_data = [0.3536539872487386, 0.5233095089594523]
# slow_lat_10_data = [0.5165612697601318, 0.32027530670166016]
# slow_lat_20_data = [5.33366674847073, 8.337077437506782]
# slow_lat_50_data = [6.686226314968533, 3.3296128114064536]
# slow_lat_70_data = [6.385747697618273, 3.037040630976359]
# slow_lat_80_data = [4.866447077857123, 1.1977286603715684]
# slow_lat_baseline = []

## p99 ##
# slow_lat_20_data = [18.755440094735885, 20.797322574456533]
# slow_lat_50_data = [9.045040104124283, 5.538473372989231]
# slow_lat_70_data = [11.727701817088656, 5.215875044133928]
# slow_lat_80_data = [8.590545836819544, 2.011797992653317]

## memory_contention##
slow_tp_5kb_data = [5133, 5390]
slow_tp_1mb_data = [5133, 5500]
slow_tp_5mb_data = [5111, 5197]
slow_tp_10mb_data = [8250, 8250]
# # slow_tp_20mb_data = [8250, 8250]
# slow_tp_baseline = [8250, 8250]

## p90 ##
# slow_lat_5kb_data = [0.3923075556755066, 0.3805748224258423]
# slow_lat_1mb_data = [0.39413084586461383, 0.3846325675646463]
# slow_lat_5mb_data = [1.0580619653066, 1.5867478410402933]
# slow_lat_10mb_data = [2.1982257088025414, 1.5626480340957645]
# # slow_lat_20mb_data = [1.3546925915612116, 1.384733862347073]
# slow_lat_baseline = [1.92584580845303, 1.92584580845303]

## p50 ##
# slow_lat_5kb_data = [0.21757817268371582, 0.28628329435984295]
# slow_lat_1mb_data = [0.322884480158488, 0.340645432472229]
# slow_lat_5mb_data = [0.36435707410176593, 0.5196836709976196]
# slow_lat_10mb_data = [1.271816333134969, 1.271816333134969]
# slow_lat_baseline = [1.271816333134969, 1.271816333134969]

## p99 ##
# slow_lat_5kb_data = [0.7859243365128835, 0.8123033273220063]
# slow_lat_1mb_data = [0.8695348143577575, 0.5272780736287434]
# slow_lat_5mb_data = [1.4321546272436778, 1.6145673855145772]
# slow_lat_10mb_data = [2.421952417294184, 2.086832249164581]
# slow_lat_baseline = [2.1867079530821907, 2.1867079530821907]


plt.figure(figsize=(7,5))

slow_20 = plt.bar(index - bar_width, slow_tp_5kb_data,
                width=bar_width, label="5 KB", color='firebrick')

slow_50 = plt.bar(index, slow_tp_1mb_data,
                width=bar_width, label="1 MB", color='#ffc406')

slow_70 = plt.bar(index + bar_width, slow_tp_5mb_data,
                width=bar_width, label="5 MB", color='royalblue')

slow_80 = plt.bar(index + 2*bar_width, slow_tp_10mb_data,
                bar_width, label="10 MB", color='seagreen')

plt.xlabel('Node Type')
plt.ylabel('Throughput (ops/sec)')
plt.title(sys.argv[2])
plt.xticks(index + bar_width/2, ["Leader", "Follower"])
plt.legend(title='Memory Limit')
plt.savefig(sys.argv[1] + '.png')