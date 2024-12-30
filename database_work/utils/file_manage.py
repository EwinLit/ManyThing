import os
from pathlib import Path

def traverse_directory(directory_path):
    """ 遍历目录并返回所有符合条件的文件路径 """
    file_paths = []
    #('.txt', '.docx', '.doc', '.pdf')
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if any(file.endswith(ext) for ext in ('.txt', '.docx', '.doc', '.pdf')):
                file_paths.append(os.path.join(root, file))
                
    return file_paths