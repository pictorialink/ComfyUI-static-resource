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
            "doodle_material": "pictorial-static-doodle",
            "poses": "pictorial-static-poses",
            "layer_material": "pictorial-static-layer",
            "style": "pictorial-static-style",
            "fonts": "pictorial-static-fonts",
            "faces": "pictorial-static-faces"
        } 
        for key, value in data.items():
            zip_url,zip_size,tag_name = get_latest_release("pictorialink", value)
           
            data[key] = {
                "tag_name": tag_name,
                "zip_url": zip_url,
                "size": zip_size,
            }
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


def get_latest_release(repo_owner, repo_name):
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    
    try:
        response = requests.get(url)
        if response.status_code == 404:
            print(f"Release not found for {repo_owner}/{repo_name}, trying tags...")
            return ""
            
        response.raise_for_status()
        release = response.json()
        print("resporeleasense", release)

        tag_name = release['tag_name']
        # tag_url = release['html_url']
        size = release['body']
        size = size.strip()
        zip_url = f"https://github.com/{repo_owner}/{repo_name}/archive/refs/tags/{tag_name}.zip"
        print(f"Latest release for {repo_name}: {tag_name} ({zip_url})")
        return zip_url,size,tag_name
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching release: {e}")
        return None, None, None
