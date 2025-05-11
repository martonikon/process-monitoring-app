import json
import psutil


def load_config(path:str = "C:\\Users\\martou\\PycharmProjects\\process-monitoring-app\\config.json")->dict:
    with open(path,"r") as f:
        return json.load(f)

def is_valid_process(proc: psutil.Process) -> bool:
    try:
        return proc.pid != 0 and proc.name() != ""
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return False


def get_process_stats() -> list[dict]:
    valid_processes = []

    for proc in psutil.process_iter(['pid', 'name']):
        if is_valid_process(proc):
            try:
                proc.cpu_percent(interval=None)
                valid_processes.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    stats = []
    for proc in valid_processes:
        try:
            stats.append({
                "pid": proc.pid,
                "name": proc.name(),
                "cpu_percent": proc.cpu_percent(interval=None),
                "memory_percent": proc.memory_percent()
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return stats