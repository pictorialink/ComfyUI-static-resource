import os
import json
CACHE_FILE = os.path.join(os.path.dirname(__file__), "../files/file_cache.json")

def load_cache():
    """加载缓存数据，如果文件不存在则返回空字典"""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_cache(data):
    """保存数据到缓存文件"""
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f, indent=2)


