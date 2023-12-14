import json
from typing import Any

def calculate_metrics(measurement: dict, context: object) -> dict[str, Any]:
    avg_cpu_util = sum(measurement[f'cpu_percent-{cpu}'] for cpu in range(context['n_cpus'])) / context['n_cpus']
    percent_network_egress = measurement['net_io_counters_eth0-bytes_sent1'] / measurement['net_io_counters_eth0-bytes_recv1'] * 100
    percent_memory_caching = (measurement['virtual_memory-cached'] + measurement['virtual_memory-buffers']) / measurement['virtual_memory-total'] * 100

    last_avg_cpu_util = context.get('last_avg_cpu_util', 0)
    alpha = 0.9
    avg_cpu_util_smoothed = alpha * last_avg_cpu_util + (1 - alpha) * avg_cpu_util

    context['last_avg_cpu_util'] = avg_cpu_util_smoothed

    result = {
        'avg-util-cpu-1min': avg_cpu_util_smoothed,
        'percent-network-egress': percent_network_egress,
        'percent-memory-caching': percent_memory_caching,
    }

    return result

def handler(input: dict, context: object) -> dict[str, Any]:
    measurement = input['metrics']
    result = calculate_metrics(measurement, context)

    result['additional_info'] = 'some_value'

    return result