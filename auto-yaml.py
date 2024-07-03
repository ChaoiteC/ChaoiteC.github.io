import os
import re
from datetime import datetime

def update_or_add_yaml_to_md_files(folder_path):
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r+', encoding='utf-8') as f:
                    content = f.read()
                    # 获取文件名作为标题（去掉扩展名）
                    title = os.path.splitext(file)[0]
                    # 获取文件的生成时间
                    creation_time = os.path.getctime(file_path)
                    date = datetime.fromtimestamp(creation_time).strftime('%Y-%m-%d %H:%M:%S')
                    
                    yaml_content = f"""---
title: "{title}"
date: "{date}"
published: false
excerpt: 自动YAML生成。正常情况下你不应该看到这个。
---"""

                    # 检查是否有YAML前置信息
                    yaml_match = re.match(r'^(---\s*\n.*?\n---\s*\n)', content, re.DOTALL)
                    if yaml_match:
                        yaml_block = yaml_match.group(1)
                        # 更新现有YAML中的日期
                        updated_yaml_block = re.sub(r'date: ".*?"', f'date: "{date}"', yaml_block)
                        updated_content = content.replace(yaml_block, updated_yaml_block, 1)
                        f.seek(0)
                        f.write(updated_content)
                        f.truncate()
                        print(f"已更新YAML时间信息到文件: {file_path}")
                    else:
                        # 写入新的YAML内容
                        f.seek(0, 0)
                        f.write(yaml_content + "\n" + content)
                        print(f"已添加YAML前置信息到文件: {file_path}")

# 指定Markdown文件夹路径（当前脚本所在文件夹）
folder_path = os.path.dirname(os.path.abspath(__file__))
update_or_add_yaml_to_md_files(folder_path)
