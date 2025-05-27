# comfyui-static-resource

## 简介
`comfyui-static-resource` 项目旨在为 ComfyUI 提供静态资源，这些资源可能包括但不限于图像、样式表、脚本文件等，用于增强 ComfyUI 的功能和视觉效果。

## 功能特性
- **资源集中管理**：将所有静态资源集中存储，方便管理和维护。
- **易于扩展**：可以轻松添加新的静态资源，满足不同的使用需求。

## 安装方法
1. 克隆本仓库到 ComfyUI 的 `custom_nodes` 目录下：
```bash
git clone https://github.com/your-repo-url/comfyui-static-resource.git /Users/duyuhang/work/github/sd/ComfyUI/custom_nodes/ComfyUI-static-resource
```
2. 重启 ComfyUI 使更改生效。

## 使用方法
目前项目引用的资源如下：

```python
data = {
    "doodle_material": "pictorial-static-doodle",
    "poses": "pictorial-static-poses",
    "layer_material": "pictorial-static-layer",
    "style": "pictorial-static-style",
    "fonts": "pictorial-static-fonts",
    "faces": "pictorial-static-faces"
} 
```


