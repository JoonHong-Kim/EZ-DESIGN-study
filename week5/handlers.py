import asyncio
import logging

from metrics import Metrics

logging.basicConfig(filename="dashboard.log", level=logging.INFO)


async def save_data(timestamp, cpu_usage, memory_usage, disk_usage):
    metrics = Metrics()
    metrics.set(
        timestamp, {"cpu": cpu_usage, "memory": memory_usage, "disk": disk_usage}
    )
    metrics.save()


async def log_to_stdout(timestamp, cpu_usage, memory_usage, disk_usage):
    if cpu_usage >= 60 or memory_usage >= 60 or disk_usage >= 60:
        print(
            f"{timestamp}: CPU={cpu_usage}%, Memory={memory_usage}%, Disk={disk_usage}%"
        )


async def log_to_file(timestamp, cpu_usage, memory_usage, disk_usage):
    if cpu_usage >= 60 or memory_usage >= 60 or disk_usage >= 60:
        logging.warn(
            f"{timestamp}: CPU={cpu_usage}%, Memory={memory_usage}%, Disk={disk_usage}%"
        )
