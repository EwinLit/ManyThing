import sqlite3
import math
from pathlib import Path
from datetime import datetime
from utils.file_manage import traverse_directory
class FileIndexAPI:
    def __init__(self, db_path='filesystem_index.db'):
        self.conn = sqlite3.connect(db_path)

    def close(self):
        """ 关闭数据库连接 """
        self.conn.close()

    def insert_file_info(self, file_path):
        """ 添加文件信息到数据库 """
        cursor = self.conn.cursor()
        
        # 获取文件信息
        path_obj = Path(file_path)
        filename = path_obj.name
        full_path = str(path_obj.absolute())
        size_kb = path_obj.stat().st_size / 1024
        modified_time = datetime.fromtimestamp(path_obj.stat().st_mtime)
        created_time = datetime.fromtimestamp(path_obj.stat().st_ctime)
        extension = path_obj.suffix[1:] if path_obj.suffix else 'none'
        
        try:
            # 插入数据
            cursor.execute('''
            INSERT INTO file_index (filename, file_path, size_kb, modified_time, created_time, extension)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (filename, full_path, size_kb, modified_time, created_time, extension))
            
            # 提交更改
            self.conn.commit()
            #print(f"Inserted info for {filename}")
        except sqlite3.IntegrityError:
            print(f"File {filename} already exists in the database.")

    def delete_file_info(self, filename):
        """ 删除指定文件的信息 """
        cursor = self.conn.cursor()
        
        # 删除文件信息
        cursor.execute('DELETE FROM file_index WHERE filename = ?', (filename,))
        
        # 提交更改
        self.conn.commit()
        #print(f"Deleted info for {filename}")

    def get_file_by_path(self, file_path):
        """ 获取指定路径的文件信息 """
        cursor = self.conn.cursor()
        
        # 查询文件信息
        cursor.execute('SELECT * FROM file_index WHERE file_path = ?', (file_path,))
        row = cursor.fetchone()
        
        if row:
            print(row)
        else:
            print("File not found.")
    # def get_all_files(self):
    #     """ 获取数据库所有文件的信息 """
    #     cursor = self.conn.cursor()
        
    #     # 查询所有文件信息
    #     cursor.execute('SELECT * FROM file_index')
    #     rows = cursor.fetchall()
        
    #     return rows
    def get_all_files(self):
        """ 获取数据库所有文件的信息 """
        cursor = self.conn.cursor()
        
        try:
            # 查询所有文件信息
            cursor.execute('SELECT * FROM file_index')
            rows = cursor.fetchall()

            # 将结果转换为字典列表，便于后续处理
            columns = [description[0] for description in cursor.description]
            files = [dict(zip(columns, row)) for row in rows]

            return files
        finally:
            # 确保关闭游标
            cursor.close()
    def display_all_files(self):
        all_files=self.get_all_files()
        if all_files:
            for file in all_files:
                print(file)
        else:
            print("No files found in the database.")
    def get_files_by_extension(self, extension):
        """ 根据扩展名获取文件信息 """
        cursor = self.conn.cursor()
        
        # 查询特定扩展名的文件信息
        cursor.execute('SELECT * FROM file_index WHERE extension = ?', (extension,))
        rows = cursor.fetchall()
        
        return rows
    
    def get_files_in_directory(self, directory_path):
        """ 获取指定目录下的所有文件信息 """
        cursor = self.conn.cursor()
        
        # 查询文件信息
        cursor.execute('SELECT * FROM file_index WHERE file_path LIKE ?', (f'{directory_path}%',))
        rows = cursor.fetchall()
        
        for row in rows:
            print(row)

    # def update_file_info(self, filename, new_size_kb=None, new_modified_time=None, new_created_time=None, new_extension=None):
    #     """ 更新指定文件的信息 """
    #     cursor = self.conn.cursor()
        
    #     updates = []
    #     params = []

    #     if new_size_kb is not None:
    #         updates.append("size_kb = ?")
    #         params.append(new_size_kb)
    #     if new_modified_time is not None:
    #         updates.append("modified_time = ?")
    #         params.append(new_modified_time)
    #     if new_created_time is not None:
    #         updates.append("created_time = ?")
    #         params.append(new_created_time)
    #     if new_extension is not None:
    #         updates.append("extension = ?")
    #         params.append(new_extension)

    #     if updates:
    #         set_clause = ", ".join(updates)
    #         query = f"UPDATE file_index SET {set_clause} WHERE filename = ?"
    #         params.append(filename)
    #         cursor.execute(query, params)
    #         self.conn.commit()
    #         print(f"Updated info for {filename}")
    #     else:
    #         print("No updates provided.")
    def delete_removed_files(self, current_paths):
        """ 删除数据库中不再存在的文件记录 """
        cursor = self.conn.cursor()
        
        # 获取数据库中所有文件路径
        cursor.execute('SELECT file_path FROM file_index')
        db_paths = set(row[0] for row in cursor.fetchall())

        # 找出数据库中存在但当前目录中不存在的文件路径
        removed_paths = db_paths - set(current_paths)

        for path in removed_paths:
            cursor.execute('DELETE FROM file_index WHERE file_path = ?', (path,))
            self.conn.commit()
            print(f"Deleted info for {Path(path).name}")
    def update_file_info_if_changed(self, file_path):
        """ 如果文件属性发生变化，则更新数据库中的记录 """
        cursor = self.conn.cursor()
        
        # 获取文件信息
        path_obj = Path(file_path)
        filename = path_obj.name
        full_path = str(path_obj.absolute())
        size_kb = path_obj.stat().st_size / 1024
        modified_time = datetime.fromtimestamp(path_obj.stat().st_mtime).isoformat(sep=' ')
        created_time = datetime.fromtimestamp(path_obj.stat().st_ctime)
        extension = path_obj.suffix[1:] if path_obj.suffix else 'none'

        # 查询数据库中的现有记录
        cursor.execute('SELECT * FROM file_index WHERE file_path = ?', (full_path,))
        row = cursor.fetchone()

        if row:
            #datatime在数据库中是字符串格式
            db_modified_time = row[3]
            db_size_kb = row[2]
            #print(f"Original db_modified_time: {db_modified_time.format(sep=' ')}")
            # 比较文件属性是否发生变化
            #if modified_time != db_modified_time or size_kb != db_size_kb:
            """浮点数精度可能导致失败"""
            size_diff = not math.isclose(size_kb, db_size_kb, rel_tol=1e-9)  # 使用相对容差比较浮点数
            time_diff = modified_time != db_modified_time.format(sep=' ')
            if time_diff or size_diff:
                # print(f"size_diff:{size_diff}")
                # print(f"time_diff:{time_diff}")
                # print(f"{filename} has changed")
                # print(f"modified_time:{modified_time}")
                # print(f"db_modified_time:{db_modified_time}")
                # print(f"dsize_kb:{db_size_kb}")
                # print(f"size_kb:{size_kb}")
                # 更新数据库中的记录
                cursor.execute('''
                UPDATE file_index SET size_kb = ?, modified_time = ?, created_time = ?, extension = ?
                WHERE file_path = ?
                ''', (size_kb, modified_time, created_time, extension, full_path))
                self.conn.commit()
                print(f"Updated info for {filename}")
            else:
                print(f"No changes detected for {filename}")
        else:
            # 文件不在数据库中，插入新记录
            self.insert_file_info(file_path)

    def update_database(self, directory_path):
        """ 更新数据库中的文件信息 """
        # 遍历文件夹并获取符合条件的文件路径
        file_paths = traverse_directory(directory_path)

        # 更新数据库中的文件信息
        for file_path in file_paths:
            self.update_file_info_if_changed(file_path)

        # 删除数据库中不再存在的文件记录
        self.delete_removed_files(file_paths)