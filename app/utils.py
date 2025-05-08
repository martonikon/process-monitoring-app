def sort_processes(data: list[dict], key: str, reverse:bool = False) -> list[dict]:
    return sorted(data, key=lambda x: x.get(key,0),reverse=reverse)

def filter_processes(data: list[dict], keyword:str)->list[dict]:
    keyword=keyword.lower()
    return [stat for stat in data if keyword in stat['name'].lower()]