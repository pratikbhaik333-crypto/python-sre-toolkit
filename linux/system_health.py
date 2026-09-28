import platform
import os
import psutil
 

def check_threshold(value, threshold):
        if value >= threshold:
            return "warning"

        else:
            return "ok"

def get_system_info():
    hostname = platform.node()
    operating_system = platform.system()
    python_version = platform.python_version()
    cpu_count = os.cpu_count()
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")
    cpu = psutil.cpu_percent()

    memory_status = check_threshold(memory.percent,80)
    disk_status = check_threshold(disk.percent,80)
    cpu_status = check_threshold(cpu,80)

    return {
        "hostname": hostname,
        "operating_system": operating_system,
        "python_version": python_version,
        "cpu_cores": cpu_count,
        "memory": {
            "percent": memory.percent,
            "status": memory_status,
            "total": memory.total,
            "available": memory.available,
            "used": memory.used,
        },
        "disk": {
            "percent": disk.percent,
            "status": disk_status,
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
        },
        "cpu": {
            "percent": cpu,
            "status": cpu_status,
        },
    }
def print_report(info):
    # Helper to convert bytes to GB with 2 decimal places
    def bytes_to_gb(b):
        return b / (1024 ** 3)
 
    hostname = info["hostname"]
    operating_system = info["operating_system"]
    python_version = info["python_version"]
    cpu_cores = info["cpu_cores"]
 
    mem = info["memory"]
    disk = info["disk"]
    cpu = info["cpu"]
 
    mem_used_gb = bytes_to_gb(mem["used"])
    mem_total_gb = bytes_to_gb(mem["total"])
    disk_used_gb = bytes_to_gb(disk["used"])
    disk_total_gb = bytes_to_gb(disk["total"])
 
    print("Python SRE check")
    print("----------------")
    print(f"Hostname: {hostname}")
    print(f"Operating System: {operating_system}")
    print(f"Python Version: {python_version}")
    print(f"CPU Cores: {cpu_cores}")
    print()
    print(
        f"Memory: {mem['percent']:.1f}% | "
        f"Used: {mem_used_gb:.2f} GB / {mem_total_gb:.2f} GB | "
        f"{mem['status'].upper()}"
    )
    print(
        f"Disk:   {disk['percent']:.1f}% | "
        f"Used: {disk_used_gb:.2f} GB / {disk_total_gb:.2f} GB | "
        f"{disk['status'].upper()}"
    )
    print(
        f"CPU:    {cpu['percent']:.1f}% | "
        f"{cpu['status'].upper()}"
    )

info = get_system_info()
print_report(info)


