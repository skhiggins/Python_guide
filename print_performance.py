# =============================================================================
# Jora
# July 20, 2022
# Python 3.10.3
# Goal: Function to print performance of script
# Input: the time when the script started running
# Output: time elapsed and environment specs (both in terminal and in csv)
# =============================================================================

import time
import sysconfig
import sys
import psutil
import multiprocessing
import pandas as pd

def print_performance(init, file = None):

    elapsed_time = time.perf_counter() - init
    if elapsed_time < 60:
        elapsed_time_str = f"{elapsed_time: 0.2f} secs"
    elif elapsed_time >= 60 and elapsed_time < 60*60:
        elapsed_time_str = f"{elapsed_time/60: 0.2f} mins"
    elif elapsed_time >= 60*60 and elapsed_time < 60*60*24:
        elapsed_time_str = f"{elapsed_time/(60*60): 0.2f} hours"
    else:
        elapsed_time_str = f"{elapsed_time/(60*60*24): 0.2f} days"

    performance = [
        elapsed_time_str,
        sysconfig.get_platform(),
        sys.version,
        f"{psutil.virtual_memory().total / 1e9: 0.2f} GB",
        multiprocessing.cpu_count()]

    indexes = [
        'Elapsed_time',
        'Platform',
        'Python_version',
        'Memory',
        'N_cores']

    performance_s = pd.Series(performance, index = indexes)

    if file is not None:
        performance_s.to_csv(file, header = False)
        print("Printed to", file)

    print(performance_s)
