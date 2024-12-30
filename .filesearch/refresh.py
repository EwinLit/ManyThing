from pathlib import Path
import extract_keywords, create_database
import sqlite3

if __name__ == "__main__":
    # 文档关键词提取
    text_path = Path.home() / "ManyThing/text_files"
    valid_extensions = {".txt", ".docx", ".pdf"}
    for file_path in text_path.rglob("*"):
        print(file_path)
        if file_path.is_file() and file_path.suffix.lower() in valid_extensions:
            output_name = file_path.stem
            extract_keywords.main(file_path, Path("./keywords") / f"{output_name}.txt")

    # 数据库创建
    # 构建文档-关键词字典
    input_directory = "keywords"
    documents, file_paths = create_database.build_documents_dictionary(input_directory)

    # 创建 SQLite 数据库
    db_path = "keywords.db"
    create_database.create_database(db_path)

    # 添加文档到数据库
    create_database.add_data_to_database(db_path, documents, file_paths)

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
