import json
import time
import folder_paths
import requests
import os
from ..services.cache import load_cache, save_cache

class StaticResource():
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": { 
                "resource_url" : ("STRING", {"default": ""}),
                "filename_prefix": ("STRING", {"default": "comfyui-static-resource"}),
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "execute2"
    OUTPUT_NODE = True
    CATEGORY = "static-resource"

    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"
        self.prefix_append = ""


    def execute(self, resource_url, filename_prefix):
        filename_prefix += self.prefix_append
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir, 0, 0)
        file = f"{filename}_{counter:05}_.zip"
        local_file_path = os.path.join(full_output_folder, file)
        print("Downloading to", local_file_path)
        download_file(resource_url, local_file_path)
        results = list()
        results.append({
            "filename": file,
            "subfolder": subfolder,
            "type": self.type
        })
        return { "ui": { "images": results } }
    
    def execute2(self, resource_url, filename_prefix):
        filename_prefix += self.prefix_append
        full_output_folder, filename, counter, subfolder, filename_prefix = folder_paths.get_save_image_path(filename_prefix, self.output_dir, 0, 0)
        file = f"{filename}_{counter:05}_.json"
        local_file_path = os.path.join(full_output_folder, file)
        cache_info = load_cache()
        print("cache_info", cache_info)
        if cache_info and "static_resource" in cache_info and "create_time" in cache_info:
            create_time = cache_info["create_time"]
            current_time = time.time()
            time_diff = current_time - create_time
            
            if time_diff < 3600 and "static_resource" in cache_info:
                print("Using cached data")
                write_to_file(cache_info["static_resource"], local_file_path)
                results = list()
                results.append({
                    "filename": file,
                    "subfolder": subfolder,
                    "type": self.type
                })
                return { "ui": { "images": results } }
            else:
                print("Cache expired, fetching new data")
                data = get_latest_release() 
        else:
            data = get_latest_release()

        cache_info["static_resource"] = data
        cache_info["create_time"] = time.time()  # 更新缓存创建时间
        save_cache(cache_info)
        write_to_file(data, local_file_path)
        print("Downloading to", local_file_path)
        results = list()
        results.append({
            "filename": file,
            "subfolder": subfolder,
            "type": self.type
        })
        return { "ui": { "images": results } }
    
    
def write_to_file(content, local_filename):
    with open(local_filename, "w", encoding="utf-8") as file:
        json.dump(content, file)

def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                f.write(chunk)
    return local_filename


def get_latest_release():
    repo_owner = "pictorialink"
    data = {
        "doodle_material": "pictorial-static-doodle",
        "poses": "pictorial-static-poses",
        "layer_material": "pictorial-static-layer",
        "style": "pictorial-static-style",
        "fonts": "pictorial-static-fonts",
        "faces": "pictorial-static-faces"
    } 
    try:
        for key, value in data.items():
            url = f"https://api.github.com/repos/{repo_owner}/{value}/releases/latest"
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Failed to fetch release for {repo_owner}/{value}, status code: {response.status_code}")
                raise ValueError("github api error, please check your network connection or the repository name")
                
            response.raise_for_status()
            release = response.json()
            print("resporeleasense", release)
            tag_name = release['tag_name']
            # tag_url = release['html_url']
            size = release['body'].strip()
            zip_url = f"https://github.com/{repo_owner}/{value}/archive/refs/tags/{tag_name}.zip"
            print(f"Latest release for {value}: {tag_name} ({zip_url})")
            data[key] = {
                "tag_name": tag_name,
                "zip_url": zip_url,
                "size": size,
            }

        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching release: {e}")
        raise ValueError("github api error, please check your network connection or the repository name") from e
