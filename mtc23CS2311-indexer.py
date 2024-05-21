import os
import sys
import lucene
import math
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, TextField, StringField
from org.apache.lucene.index import IndexWriter, IndexWriterConfig
from org.apache.lucene.store import MMapDirectory
from java.nio.file import Paths
import logging

lucene.initVM(vmargs=['-Djava.awt.headless=true'])

logging.basicConfig(filename='indexing_log.txt', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

def custom_term_weight(term_freq, total_terms, m=0.9, λ=0.4):
    if total_terms == 0:
        return 0  # Avoid division by zero if there are no terms

    normalized_tf = term_freq / total_terms if total_terms > 0 else 0
    x = normalized_tf
    f_t0 = normalized_tf

    if f_t0 == 0:
        return 0
    
    z = -λ * (1 - m) * x + (f_t0 ** (1 - m))

    if m == 1:
        return (1 / λ) * f_t0 * (1 - math.exp(-λ * x))
    elif m == 2:
        return (1 / λ) * (math.log(f_t0) - (1 / (1 - m)) * math.log(z))
    else:
        return (1 / (λ * (2 - m))) * ((f_t0 ** (2 - m)) - (z ** ((2 - m) / (1 - m))))

def index_documents(docs_path, index_path):
    analyzer = StandardAnalyzer()
    index_dir = MMapDirectory(Paths.get(index_path))
    config = IndexWriterConfig(analyzer)
    writer = IndexWriter(index_dir, config)

    doc_count = 0
    failed_count = 0
    for doc in os.listdir(docs_path):
        try:
            with open(os.path.join(docs_path, doc), 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()
                # Extract DOCNO as document ID
                doc_id_start = content.find('<DOCNO>') + 7
                doc_id_end = content.find('</DOCNO>')
                doc_id = content[doc_id_start:doc_id_end].strip()
                
                document = Document()
                total_terms = len(content.split())  # Simple word count
                term_freq = content.count("specific_term")  # Frequency of a specific term
                term_weight = custom_term_weight(term_freq, total_terms)
                document.add(TextField("content", content, Field.Store.YES))
                document.add(StringField("doc_id", doc_id, Field.Store.YES))  # Use doc_id as the document ID
                writer.addDocument(document)
                doc_count += 1
                logging.info(f"Successfully indexed document ID: {doc_id}")
        except Exception as e:
            failed_count += 1
            logging.error(f"Failed to index document {doc_id}: {str(e)}")

    writer.close()
    print(f"Indexed {doc_count} documents from {docs_path} into {index_path}")
    print(f"Failed to index {failed_count} documents.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python mtc23CS2316-indexer.py <docs_path> <index_path>")
        sys.exit(1)
    docs_path = sys.argv[1]
    index_path = sys.argv[2]
    index_documents(docs_path, index_path)