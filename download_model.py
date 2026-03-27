#!/usr/bin/env python
"""下载 HuggingFace 模型到本地目录"""

from huggingface_hub import snapshot_download
import os

# 模型名称
model_name = "BAAI/bge-base-zh-v1.5"

# 下载到当前项目的 models 目录
local_dir = os.path.join(os.getcwd(), "models", "bge-base-zh-v1.5")
os.makedirs(local_dir, exist_ok=True)

print(f"正在下载模型: {model_name}")
print(f"保存到: {local_dir}")

try:
    snapshot_download(
        repo_id=model_name,
        local_dir=local_dir,
        local_dir_use_symlinks=False,  # 禁用符号链接，避免 Windows 问题
        resume_download=True
    )
    print(f"✅ 模型下载成功！保存到: {local_dir}")
except Exception as e:
    print(f"❌ 下载失败: {e}")
    print("\n请检查网络连接，或手动下载模型到上述目录")
