import time
import psutil

def get_system_kpis():
    boot_time = psutil.boot_time()
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    return {
        "uptime": int(time.time() - boot_time),
        "cpu": psutil.cpu_percent(),
        "ram": ram.percent,
        "ram_used": ram.used,
        "ram_total": ram.total,
        "disk": disk.percent,
        "disk_used": disk.used,
        "disk_total": disk.total,
    }