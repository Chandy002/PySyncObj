from __future__ import print_function
from asyncio.subprocess import PIPE
import sys
from subprocess import Popen
import time
import random
from collections import defaultdict
sys.path.append("../")
from pysyncobj import SyncObj, replicated, SyncObjConf, FAIL_REASON
import numpy as np

class TestObj(SyncObj):

    def __init__(self, selfNodeAddr, otherNodeAddrs):
        cfg = SyncObjConf(
            appendEntriesUseBatch=False,
        )
        super(TestObj, self).__init__(selfNodeAddr, otherNodeAddrs, cfg)
        self.__appliedCommands = 0

    @replicated
    def testMethod(self, val, callTime):
        self.__appliedCommands += 1
        return (callTime, time.time())

    def getNumCommandsApplied(self):
        return self.__appliedCommands

_g_sent = 0
_g_success = 0
_g_error = 0
_g_errors = defaultdict(int)
_g_delays = []

def clbck(res, err):
    global _g_error, _g_success, _g_delays
    if err == FAIL_REASON.SUCCESS:
        _g_success += 1
        callTime, recvTime = res
        delay = time.time() - callTime
        _g_delays.append(delay)
    else:
        _g_error += 1
        _g_errors[err] += 1

def getRandStr(l):
    f = '%0' + str(l) + 'x'
    return f % random.randrange(16 ** l)

if __name__ == '__main__':
    try:
        if len(sys.argv) < 5:
            print('Usage: %s RPS requestSize selfHost:port partner1Host:port partner2Host:port ...' % sys.argv[0])
            sys.exit(-1)

        numCommands = int(sys.argv[1])
        cmdSize = int(sys.argv[2])
        cpu = int(sys.argv[3])

        selfAddr = sys.argv[4]
        if selfAddr == 'readonly':
            selfAddr = None
        partners = sys.argv[5:]

        maxCommandsQueueSize = int(0.9 * SyncObjConf().commandsQueueSize / len(partners))

        obj = TestObj(selfAddr, partners)

        while obj._getLeader() is None:
            time.sleep(0.5)

        ## get thread native id
        t_id = obj.get_thread().native_id
        # pin_node_cmd = f"taskset -cp {cpu} {t_id}"
        # p = Popen(['/bin/bash', '-c', pin_node_cmd], stdout=PIPE)

        # write leader info to file named 'leader' + selfAddr.split(':')[1]
        with open('leader' + selfAddr.split(':')[1], 'w') as f:
            f.write('Leader ' + obj._getLeader().address)
            f.write('\nThreadId ' + str(t_id))

        time.sleep(4.0)

        startTime = time.time()

        while time.time() - startTime < 25.0:
            st = time.time()
            for i in range(0, numCommands):
                obj.testMethod(getRandStr(cmdSize), time.time(), callback=clbck)
                _g_sent += 1
            delta = time.time() - st
            assert delta <= 1.0
            time.sleep(1.0 - delta)

        time.sleep(4.0)

        successRate = float(_g_success) / 25.0
        print('THROUGHPUT:', successRate)

        delays = sorted(_g_delays)
        avgDelay = _g_delays[int(len(_g_delays) / 2)]
        # print('DELAYS:', _g_delays)
        print('AVG LATENCY:', avgDelay)        
        print('P90 LATENCY:', np.percentile(delays, 90))
        print('P99 LATENCY:', np.percentile(delays, 99))
    except Exception as e:
        print(e)
        sys.exit(-1)