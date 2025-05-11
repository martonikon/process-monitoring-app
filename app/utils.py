import psutil

def sort_processes(data: list[dict], key: str, reverse:bool = False) -> list[dict]:
    return sorted(data, key=lambda x: x.get(key,0),reverse=reverse)

def filter_processes(data: list[dict], keyword:str)->list[dict]:
    keyword=keyword.lower()
    return [proc for proc in data if keyword in proc['name'].lower()]

def mark_child_processes(data: list[dict])-> list[dict]:
    pid_set = {proc["pid"] for proc in data}
    pid_to_ppid={}

    for proc in psutil.process_iter(['pid','ppid']):
        try:
            pid_to_ppid[proc.info["pid"]] = proc.info["ppid"]
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    for proc in data:
        ppid = pid_to_ppid.get(proc["pid"])
        proc["is_child"] = ppid in pid_set if ppid is not None else False

    return data

def detect_anomalies(data, cpu_threshold=80.0, mem_threshold=80.0):
    anomalies=[]
    for stat in data:
        if stat["cpu_percent"] >= cpu_threshold or stat['memory_percent'] >= mem_threshold:
            anomalies.append(stat)
    return anomalies

