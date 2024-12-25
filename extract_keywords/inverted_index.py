from whoosh.fields import Schema, TEXT, ID
from whoosh.index import create_in
from whoosh.qparser import QueryParser
from whoosh.index import open_dir
from pathlib import Path
import argparse

# Define index structure
def create_index(index_dir):
    index_path = Path(index_dir)
    schema = Schema(
        doc_id=ID(stored=True, unique=True), # Document ID
        content=TEXT(stored=True) # Document keywords (full text searchable)
    )

    if not index_path.exists():
        index_path.mkdir(parents=True)

    return create_in(index_path, schema)

# Add documents to index
def add_documents_to_index(index_dir, documents):
    index_path = Path(index_dir)
    ix = open_dir(str(index_path))
    writer = ix.writer()

    for doc_id, keywords in documents.items():
        writer.add_document(doc_id=str(doc_id), content=" ".join(keywords))
    writer.commit()

# Keyword search
def search_keywords(index_dir, query_str):
    index_path = Path(index_dir)
    ix = open_dir(str(index_path))
    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(query_str)
        results = searcher.search(query, limit=10)
        return [result["doc_id"] for result in results]
    
# Build documents-kerwords dictionary
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
    # Construct the document and its extracted keywords into a dictionary
    input_directory = "keywords"
    documents = build_documents_dictionary(input_directory)

    # Create index directory
    index_directory = Path("index")
    create_index(index_directory)

    # Add documents to index
    add_documents_to_index(index_directory, documents)

    # Search keywords
    parser = argparse.ArgumentParser(description="Search for keywords in the indexed documents.")
    parser.add_argument("--search_query", type=str, help="The keyword or phrase to search for.")
    args = parser.parse_args()

    search_query = args.search_query
    results = search_keywords(index_directory, search_query)

    print(f"Documents matching '{search_query}': {results}")