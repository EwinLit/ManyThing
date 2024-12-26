import os
from pathlib import Path
from database.file_index_api import FileIndexAPI
import argparse
from utils.file_manage import traverse_directory
from database.database_setup import initialize_database

def main(directory_path):
    # 指定要索引的文件扩展名
    #extensions = ('.txt', '.docx', '.doc', '.pdf')
    
    # 初始化数据库

    initialize_database()

    # 创建 API 实例
    api = FileIndexAPI()

    try:
        # 遍历文件夹并获取符合条件的文件路径
        file_paths = traverse_directory(directory_path)

        # 插入文件信息到数据库
        for file_path in file_paths:
            #print(f"Processing file: {file_path}")
            api.insert_file_info(file_path)
        
        #print("All files processed and indexed.")
        api.display_all_files()
        api.update_database(directory_path)
    finally:
        # 关闭数据库连接
        api.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="遍历指定文件夹下的所有 txt、docx、doc、pdf 文件，并建立数据库索引")
    parser.add_argument('directory_path', type=str, help='要遍历的文件夹路径')
    # 解析命令行参数
    args = parser.parse_args()

    # 调用 main 函数并传递命令行参数
    main(args.directory_path)
    