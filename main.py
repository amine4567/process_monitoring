import argparse
from collections import OrderedDict
import datetime
import os
from subprocess import Popen
import time

import psutil

parser = argparse.ArgumentParser()
parser.add_argument("sh_command")
args = parser.parse_args()

process_id = Popen(args=args.sh_command.split()).pid

process = psutil.Process(process_id)

columns = OrderedDict(
    [
        ("timestamp_utc", datetime.datetime.utcnow()),
        ("resident_memory", 0.0),
        ("shared_memory", 0.0),
        ("not_shared_memory", 0.0),
        ("swap_memory", 0.0),
    ]
)


if not os.path.exists("log_file.csv"):
    with open("log_file.csv", "w") as file:
        file.write((",".join(columns.keys()) + "\n"))

while True:
    columns["timestamp_utc"] = datetime.datetime.utcnow()

    process_mem_info = process.memory_full_info()

    # Memory in MiB
    columns["resident_memory"] = process_mem_info.rss / (2 ** 20)
    columns["shared_memory"] = process_mem_info.shared / (2 ** 20)
    columns["not_shared_memory"] = columns["resident_memory"] - columns["shared_memory"]
    columns["swap_memory"] = process_mem_info.swap / (2 ** 20)

    info_line = ",".join(f"{col_info}" for col_info in columns.values()) + "\n"
    with open("log_file.csv", "a") as file:
        file.write(info_line)

    time.sleep(1)
