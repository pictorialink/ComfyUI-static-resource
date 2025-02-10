import json
import folder_paths
import requests
import os

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
        data = {
            "doodle_material": "https://github.com/solution9th/pictorial-static-doodle/archive/refs/heads/main.zip",
            "poses": "https://github.com/solution9th/pictorial-static-poses/archive/refs/heads/main.zip",
            "layer_material": "https://github.com/solution9th/pictorial-static-layer/archive/refs/heads/main.zip",
            "style": "https://github.com/solution9th/pictorial-static-style/archive/refs/heads/main.zip",
            "fonts": "https://github.com/solution9th/pictorial-static-fonts/archive/refs/heads/main.zip",
            "faces": "https://github.com/solution9th/pictorial-static-faces/archive/refs/heads/main.zip"
        } 
        write_to_file(data, local_file_path)
        results = list()
        results.append({
            "filename": file,
            "subfolder": subfolder,
            "type": self.type
        })
        return { "ui": { "images": results } }
    
    
def write_to_file(content, local_filename):
    with open(local_filename, "w", encoding="utf-8") as file:
        json.dump(content, file)  # indent 参数用于美化输出，缩进 4 个空格

def download_file(url, local_filename):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                f.write(chunk)
    return local_filename