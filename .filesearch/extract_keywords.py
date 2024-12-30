import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from PyPDF2 import PdfReader
from docx import Document
from transformers import pipeline, BartTokenizer
from pathlib import Path

import sqlite3

# Read different types of text documents
def read_text(file_path):
    if file_path.suffix == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    elif file_path.suffix == ".pdf":
        reader = PdfReader(file_path)
        return " ".join(page.extract_text() for page in reader.pages)
    elif file_path.suffix == ".docx":
        doc = Document(file_path)
        return " ".join(paragraph.text for paragraph in doc.paragraphs)
    else:
        raise ValueError("Unsupported file format. Use txt, pdf, or docx.")
    
# Extract keywords using DistilBERT
def extract_keywords(text, top_k=10):
    # Load DistilBERT pretrained model
    summarizer = pipeline("summarization", model="./distilbart-cnn-12-6")
    tokenizer = BartTokenizer.from_pretrained("./bart-large-cnn")

    # Define the maximum input length for the model
    max_input_length = 1000  # This depends on the model, for distilBART it's 1024 tokens
    
    # Tokenize the input text to split into smaller chunks if it's too long
    tokens = tokenizer.encode(text, truncation=False)
    chunks = [tokens[i:i + max_input_length] for i in range(0, len(tokens), max_input_length)]
    
    summary_text = ""
    for chunk in chunks:
        # Join chunk back into a string and summarize it
        chunk_text = tokenizer.decode(chunk, skip_special_tokens=True)
        summary = summarizer(chunk_text, max_length=1000, min_length=10, do_sample=False)
        summary_text += summary[0]['summary_text'] + " "  # Concatenate summaries

    # Word segmentation and stop word filtering
    words = word_tokenize(summary_text)
    filtered_words = [word.lower() for word in words if word.isalnum()]
    stop_words = set(stopwords.words("english"))
    keywords = [word for word in filtered_words if word not in stop_words]

    # Sort by frequency, top_k keywords
    keyword_freq = {word: keywords.count(word) for word in set(keywords)}
    sorted_keywords = sorted(keyword_freq, key=keyword_freq.get, reverse=True)
    
    return sorted_keywords[:top_k]

# 保存关键词到数据库
def save_keywords_to_db(db_path, file_path, keywords):
    # 连接到 SQLite 数据库（如果数据库不存在会自动创建）
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 创建表格（如果表格不存在）
    cursor.execute('''CREATE TABLE IF NOT EXISTS ori_keywords (
                        path TEXT PRIMARY KEY,
                        keywords TEXT
                    )''')

    # 将关键词保存到数据库，关键词转换为字符串形式
    keywords_str = ", ".join(keywords)
    cursor.execute("REPLACE INTO ori_keywords (path, keywords) VALUES (?, ?)", (str(file_path), keywords_str))
    
    # 提交并关闭连接
    conn.commit()
    conn.close()

def main(input_file, db_path, top_k=10):
    text = read_text(input_file)
    keywords = extract_keywords(text, top_k=top_k)
    save_keywords_to_db(db_path, input_file, keywords)
    print(f"Keywords for {input_file} saved to database.")

'''
if __name__ == "__main__":
    text_path = Path("./text_files")
    valid_extensions = {".txt", ".docx", ".pdf"}
    for file_path in text_path.rglob("*"):
        if file_path.is_file and text_path.suffix.lower() in valid_extensions:
            output_name = file_path.stem
            main(file_path, Path("./keywords") / f"{output_name}.txt")
'''