import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from PyPDF2 import PdfReader
from docx import Document
from transformers import pipeline
from pathlib import Path

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
    summary = summarizer(text, max_length=100, min_length=30, do_sample=False)

    # Word segmentation and stop word filtering
    words = word_tokenize(summary[0]['summary_text'])
    filtered_words = [word.lower() for word in words if word.isalnum()]
    stop_words = set(stopwords.words("english"))
    keywords = [word for word in filtered_words if word not in stop_words]

    # Sort by frequency, top_k keywords
    keyword_freq = {word: keywords.count(word) for word in set(keywords)}
    sorted_keywords = sorted(keyword_freq, key=keyword_freq.get, reverse=True)
    return sorted_keywords[:top_k]

def save_keywords(keywords, output_file):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(keywords))

def main(input_file, output_file, top_k=10):
    text = read_text(input_file)
    keywords = extract_keywords(text, top_k=top_k)
    save_keywords(keywords, output_file)
    print(f"Keywords saved to {output_file}")

if __name__ == "__main__":
    text_path = Path("./text_files")
    for file_path in text_path.rglob("*"):
        if file_path.is_file():
            output_name = file_path.stem
            main(file_path, Path("./keywords") / f"{output_name}.txt")