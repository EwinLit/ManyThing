import sqlite3
from pathlib import Path
import argparse

# 创建 SQLite 数据库和表
def create_database(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # 创建表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS keyword_to_file (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT NOT NULL,
            doc_id TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# 添加文档及其关键词到数据库
def add_data_to_database(db_path, documents):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM keyword_to_file")
    for doc_id, keywords in documents.items():
        for keyword in keywords:
            # 检查是否已存在相同的关键词-文件名对
            cursor.execute('''
                SELECT 1 FROM keyword_to_file WHERE keyword = ? AND doc_id = ?
            ''', (keyword, doc_id))
            if cursor.fetchone() is None:
                # 插入数据
                cursor.execute('''
                    INSERT INTO keyword_to_file (keyword, doc_id) VALUES (?, ?)
                ''', (keyword, doc_id))
    conn.commit()
    conn.close()

# 根据关键词检索文档
def search_keywords(db_path, query_str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    #query = f"%{query_str}%"
    cursor.execute('''
        SELECT doc_id FROM keyword_to_file WHERE keyword = ?
    ''', (query_str,))
    results = cursor.fetchall()
    conn.close()
    return [result[0] for result in results]

# 从文件夹构建文档-关键词字典
def build_documents_dictionary(input_dir):
    documents = {}
    input_path = Path(input_dir)

    for file_path in input_path.glob("*.txt"):
        doc_id = file_path.stem
        with file_path.open("r", encoding="utf-8") as f:
            keywords = [line.strip() for line in f.readlines() if line.strip()]

        documents[doc_id] = keywords
    
    return documents

if __name__ == "__main__":
    # 构建文档-关键词字典
    input_directory = "keywords"
    documents = build_documents_dictionary(input_directory)

    # 创建 SQLite 数据库
    db_path = "documents.db"
    create_database(db_path)

    # 添加文档到数据库
    add_data_to_database(db_path, documents)

    conn = conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 查询所有数据
    cursor.execute("SELECT * FROM keyword_to_file")
    rows = cursor.fetchall()

    # 打印数据
    for row in rows:
        print(row)

    # 关闭连接
    conn.close()

    # 解析命令行参数进行关键词检索
    parser = argparse.ArgumentParser(description="Search for keywords in the SQLite database.")
    parser.add_argument("--search_query", type=str, help="The keyword or phrase to search for.")
    args = parser.parse_args()

    search_query = args.search_query
    if search_query:
        results = search_keywords(db_path, search_query)
        print(f"Documents matching '{search_query}': {results}")
