def sort_processes(data: list[dict], key: str, reverse:bool = False) -> list[dict]:
    return sorted(data, key=lambda x: x.get(key,0),reverse=reverse)

def filter_processes(data: list[dict], keyword:str)->list[dict]:
    keyword=keyword.lower()
    return [stat for stat in data if keyword in stat['name'].lower()]

def detect_anomalies(data, cpu_threshold=80.0, mem_threshold=80.0):
    anomalies=[]
    for stat in data:
        if stat["cpu_percent"] >= cpu_threshold or stat['memory_percent'] >= mem_threshold:
            anomalies.append(stat)
    return anomalies