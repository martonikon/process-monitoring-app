import json
import psutil

def load_config(path:str = "C:\\Users\\martou\\PycharmProjects\\process-monitoring-app\\config.json")->dict:
    with open(path,"r") as f:
        return json.load(f)


def get_process_stats() -> list[dict]:
    list_of_stats=[]
    for stat in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            info=stat.info
            list_of_stats.append({
                "pid": info['pid'],
                "name": info['name'],
                "cpu_percent": info['cpu_percent'],
                "memory_percent": info['memory_percent']
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return list_of_stats