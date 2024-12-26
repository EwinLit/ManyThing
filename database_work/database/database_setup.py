import sqlite3
from pathlib import Path
from datetime import datetime

def initialize_database(db_path='filesystem_index.db'):
    """ 初始化数据库并创建表 """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 创建表
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS file_index (
        filename TEXT PRIMARY KEY,
        file_path TEXT NOT NULL,
        size_kb REAL NOT NULL,
        modified_time TIMESTAMP NOT NULL,
        created_time TIMESTAMP NOT NULL,
        extension TEXT NOT NULL
    )
    ''')

    # 提交更改并关闭连接
    conn.commit()
    conn.close()

