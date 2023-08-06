import psutil
import platform
from datetime import datetime


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def seconds_convert(seconds): 
    min, sec = divmod(seconds, 60) 
    hour, min = divmod(min, 60) 
    return "%d:%02d:%02d" % (hour, min, sec) 


def system_information():
    uname = platform.uname()
    return {
       "System": uname.system,
       "Node Name": uname.node,
       "Release": uname.release,
       "Version": uname.version,
       "Machine": uname.machine,
       "Processor": uname.processor
    }

def boot_time():
    boot_time_timestamp = psutil.boot_time()
    converted_date = datetime.fromtimestamp(boot_time_timestamp)
    return {
        "year": converted_date.year,
        "month": converted_date.month,
        "day": converted_date.day,
        "hour": converted_date.hour,
        "minute": converted_date.minute,
        "second": converted_date.second
    }


def cpu_info():
    cpufreq = psutil.cpu_freq()

    params = {
        "Physical Cores": psutil.cpu_count(logical=False),
        "Total Cores": psutil.cpu_count(logical=True),
        "Maximum Frequency": f"{cpufreq.max:.2f}Mhz",
        "Minimum Frequency": f"{cpufreq.min:.2f}Mhz",
        "Current Frequency": f"{cpufreq.current:.2f}Mhz"
    }

    params['Cores'] = {}
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        params['Cores'][f"Core {i}"] = f"{percentage}%"
    
    params["Total CPU Usage"] = f"{psutil.cpu_percent()}%"

    return params 


def virtual_memory():
    svmem = psutil.virtual_memory()
    return {
        "Total": get_size(svmem.total),
        "Available":  get_size(svmem.available),
        "Used": get_size(svmem.used),
        "Percentage": f"{svmem.percent}%"
    }

def swap_memory():
    swap = psutil.swap_memory()
    return {
        "Total": get_size(swap.total),
        "Free": get_size(swap.free),
        "Used": get_size(swap.used),
        "Percentage": f"{swap.percent}%"
    }


def disk_info():
    partitions = psutil.disk_partitions()
    params = {"Partitions": {}}
    for partition in partitions:
        params["Partitions"][partition.device] = {
            "MountPoint": partition.mountpoint,
            "File System Type": partition.fstype
        }
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
            params["Partitions"][partition.device].update({"Partition Usage":{
                "Total Size": get_size(partition_usage.total),
                "Used": get_size(partition_usage.used),
                "Free": get_size(partition_usage.free),
                "Percentage": f"{partition_usage.percent}%"
            }})
        except PermissionError:
            continue

    disk_io = psutil.disk_io_counters()
    params["Total Read"] = get_size(disk_io.read_bytes)
    params["Total Write"] = get_size(disk_io.write_bytes)

    return params

def network_info():
    params = {}
    if_addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in if_addrs.items():
        for address in interface_addresses:
            if str(address.family) == 'AddressFamily.AF_INET':
                params["IP Address"] = address.address,
                params["Netmask"] = address.netmask,
                params["Broadcast IP"] = address.broadcast,
            elif str(address.family) == 'AddressFamily.AF_PACKET':
                params["MAC Address"] = address.address,
                params["Netmask"] = address.netmask,
                params["Broadcast MAC"] = address.broadcast

    net_io = psutil.net_io_counters()
    params["Total Bytes Sent"] = get_size(net_io.bytes_sent)
    params["Total Bytes Received"] = get_size(net_io.bytes_recv)

    return params

def battery_info():
    try:
        battery_stats = psutil.sensors_battery()
        plugged = "Yes" if battery_stats.power_plugged else "No"
        percentage_left = battery_stats.percent
        seconds_left = seconds_convert(battery_stats.secsleft)
        if seconds_left[0] == '-':
            seconds_left = seconds_left[1:]
    except Exception as e:
        print(e)
        return {"error": e}
    
    return {
        "Percentage": f"{percentage_left:.2f}%",
        "Plugged Status": plugged,
        "Seconds Left to Discharge": seconds_left
    }


def temperature_info():
    # try:
    #     temperature_stats = psutil.sensors_temperatures()
    #     params = {}
    #     for i in temperature_stats.keys():
    #         if i == 'coretemp':
    #             params['Core Temperature'] = {}
    #             for j in i:
    #                 print(j)
    #                 params['Core Temperature'].update({j.label:{'current':j.current}})  
    #                 params['Core Temperature'].update({j.label:{'high':j.high}})
    #                 params['Core Temperature'].update({j.label:{'critical':j.critical}})
    #     print(params)
    # except Exception as e:
    #     print(e)
    return psutil.sensors_temperatures()

#print(psutil.sensors_temperatures())
