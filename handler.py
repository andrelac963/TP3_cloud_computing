from typing import Any


def handler(input: dict, context: object) -> dict[str, Any]:

    timestamp = input["timestamp"]
    bytes_sent = input["net_io_counters_eth0-bytes_sent1"]
    bytes_recv = input["net_io_counters_eth0-bytes_recv1"]
    total_memory = input["virtual_memory-total"]
    cached_memory = input["virtual_memory-cached"]
    buffer_memory = input["virtual_memory-buffers"]

    percent_outgoing_traffic = bytes_sent / (bytes_sent + bytes_recv) * 100
    percent_memory_caching = (cached_memory + buffer_memory) / total_memory * 100

    moving_average_cpu_utilization = []
    for cpu_utilization in input["cpu_percent-X"]:
        moving_average_cpu_utilization.append(cpu_utilization)
    if len(moving_average_cpu_utilization) > 60:
        moving_average_cpu_utilization.pop(0)
    moving_average_cpu_utilization = sum(moving_average_cpu_utilization) / len(moving_average_cpu_utilization)

    output_data = {
        "timestamp": timestamp,
        "percent_outgoing_traffic": percent_outgoing_traffic,
        "percent_memory_caching": percent_memory_caching,
        "moving_average_cpu_utilization": moving_average_cpu_utilization,
    }
    return output_data
