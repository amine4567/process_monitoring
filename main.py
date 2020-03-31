import argparse
import os
import time
import datetime
import subprocess

import psutil

parser = argparse.ArgumentParser()
parser.add_argument("sh_command")
args = parser.parse_args()

process_id = subprocess.Popen(args=[args.sh_command]).pid
print(process_id)

process = psutil.Process(process_id)

if not os.path.exists("log_file.csv"):
    with open("log_file.csv", "w") as file:
        file.write(
            (
                "timestamp_utc, resident_mememory (MiB), shared_memory (MiB), not_shared_memory (MiB) \n"
            )
        )

while True:
    timestamp_utc = datetime.datetime.utcnow()

    process_mem_info = process.memory_info()

    # Memory in MiB
    resident_mem = process_mem_info.rss / (2 ** 20)
    shared_mem = process_mem_info.shared / (2 ** 20)
    not_shared_mem = resident_mem - shared_mem

    mem_info_line = (
        f"{timestamp_utc}, {resident_mem}, {shared_mem}, {not_shared_mem} \n"
    )
    with open("log_file.csv", "a") as file:
        file.write(mem_info_line)

    # print(mem_info_line)

    time.sleep(1)
