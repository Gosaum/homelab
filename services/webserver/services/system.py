import psutil

def get_cpu_percent():
    return psutil.cpu_percent(interval=None) # measures the load since the previous call