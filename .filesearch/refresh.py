from pathlib import Path
import extract_keywords, create_database
import sqlite3

if __name__ == "__main__":
    # 文档关键词提取
    text_path = Path("text_files")
    ori_db_path = Path("./ori_keywords.db")
    db_path = Path("./keyword.db")

    valid_extensions = {".txt", ".docx", ".pdf"}
    for file_path in text_path.rglob("*"):
        print(f"Processing file: {file_path}")
        if file_path.is_file() and file_path.suffix.lower() in valid_extensions:
            extract_keywords.main(file_path.resolve(), ori_db_path)
            conn = sqlite3.connect(ori_db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT keywords FROM ori_keywords WHERE path = ?", (str(file_path),))
            result = cursor.fetchone()

            if result:
                keywords = result[0].split(", ")
                print(f"Extracted keywords: {keywords}")
            else:
                print("No keywords found in database.")

            conn.close()

    # 数据库创建
    create_database.build_inverted_index_from_keyword_db(ori_db_path, db_path)

    inv_conn = sqlite3.connect(db_path)
    inv_cursor = inv_conn.cursor()

    # 查询所有数据
    inv_cursor.execute("SELECT * FROM keyword")
    rows = inv_cursor.fetchall()

    # 打印数据
    print("\n倒排索引数据库内容：")
    for row in rows:
        print(row)

    # 关闭连接
    inv_conn.close()
