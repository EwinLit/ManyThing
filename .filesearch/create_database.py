import sqlite3
from pathlib import Path
import argparse

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

# 创建 SQLite 数据库和表
def create_database(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # 删除表格（如果表格已存在）
    cursor.execute('''DROP TABLE IF EXISTS keyword''')
    # 创建表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS keyword (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL,
            name TEXT NOT NULL,
            path TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# 添加文档及其关键词到数据库
def add_data_to_database(db_path, documents, file_paths):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM keyword")
    for doc_id, keywords in documents.items():
        file_path = file_paths[doc_id]
        for keyword in keywords:
            # 检查是否已存在相同的关键词-文件名对
            cursor.execute('''
                SELECT 1 FROM keyword WHERE word = ? AND name = ? AND path = ?
            ''', (keyword, doc_id, file_path))
            if cursor.fetchone() is None:
                # 插入数据
                cursor.execute('''
                    INSERT INTO keyword (word, name, path) VALUES (?, ?, ?)
                ''', (keyword, doc_id, file_path))
    conn.commit()
    conn.close()

# 根据关键词检索文档
def search_keywords(db_path, query_str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    #query = f"%{query_str}%"
    cursor.execute('''
        SELECT name FROM keyword WHERE word = ?
    ''', (query_str,))
    results = cursor.fetchall()
    conn.close()
    return [result[0] for result in results]

# 从文件夹构建文档-关键词字典
def build_documents_dictionary(input_dir):
    documents = {}
    file_paths = {}
    input_path = Path(input_dir)

    for file_path in input_path.glob("*.txt"):
        doc_id = file_path.stem
        with file_path.open("r", encoding="utf-8") as f:
            keywords = [line.strip() for line in f.readlines() if line.strip()]

        documents[doc_id] = keywords
        file_paths[doc_id] = str(file_path.resolve())
    
    return documents, file_paths

# 提取自然语言中的关键词
def extract_keywords_from_nl(nl_query):
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(nl_query)
    keywords = [word.lower() for word in words if word.isalnum() and word.lower() not in stop_words]
    return keywords
'''
if __name__ == "__main__":
    # 构建文档-关键词字典
    input_directory = "keywords"
    documents = build_documents_dictionary(input_directory)

    # 创建 SQLite 数据库
    db_path = "keywords.db"
    create_database(db_path)

    # 添加文档到数据库
    add_data_to_database(db_path, documents)

    conn = conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 查询所有数据
    cursor.execute("SELECT * FROM keyword")
    rows = cursor.fetchall()

    # 打印数据
    for row in rows:
        print(row)

    # 关闭连接
    conn.close()

    # 解析命令行参数进行关键词检索
    parser = argparse.ArgumentParser(description="Search for keywords in the SQLite database.")
    parser.add_argument("--search_query", type=str, help="The keyword or phrase to search for.")
    parser.add_argument("--nl_query", type=str, help="The natural language query to extract keywords from.")
    args = parser.parse_args()

    search_query = args.search_query
    if args.search_query:
        results = search_keywords(db_path, args.search_query)
        print(f"Documents matching '{args.search_query}': {results}")

    if args.nl_query:
        keywords = extract_keywords_from_nl(args.nl_query)
        print(f"Extracted keywords: {keywords}")
        all_results = []
        for keyword in keywords:
            results = search_keywords(db_path, keyword)
            all_results.extend(results)
        print(f"Documents matching natural language query '{args.nl_query}': {list(set(all_results))}")
'''
