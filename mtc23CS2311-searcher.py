import os
import sys
import lucene
import xml.etree.ElementTree as ET
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser, QueryParserBase
from org.apache.lucene.search import IndexSearcher, ScoreDoc
from org.apache.lucene.store import MMapDirectory
from java.nio.file import Paths

lucene.initVM(vmargs=['-Djava.awt.headless=true'])

def escape_query(query):
    return QueryParserBase.escape(query)

def search_index(index_path, query_file_path, output_file_path, rollno):
    analyzer = StandardAnalyzer()
    index_dir = MMapDirectory(Paths.get(index_path))
    reader = DirectoryReader.open(index_dir)
    searcher = IndexSearcher(reader)

    print(f"Index directory: {index_path}")
    print(f"Query file path: {query_file_path}")
    print(f"Output file path: {output_file_path}")
    tree = ET.parse(query_file_path)
    root = tree.getroot()

    with open(output_file_path, 'w') as output_file:
        for top in root.findall('top'):
            qid = top.find('num').text.strip()
            title = top.find('title').text.strip()
            escaped_title = escape_query(title)
            query = QueryParser("content", analyzer).parse(escaped_title)
            hits = searcher.search(query, 1000).scoreDocs

            print(f"Query ID: {qid}, Title: '{title}', Escaped Title: '{escaped_title}', Hits: {len(hits)}")
            seen_docs = set()
            for rank, hit in enumerate(hits):
                doc = searcher.doc(hit.doc)
                doc_id = doc.get("doc_id")  # Directly use the doc_id from the document

                if (qid, doc_id) in seen_docs:
                    continue  # Skip this doc since it's already been processed for this query
                seen_docs.add((qid, doc_id))

                score = hit.score
                print(f"Doc ID: {doc_id}, Rank: {rank + 1}, Score: {score}")
                output_file.write(f"{qid}\tQ0\t{doc_id:<10}\t{rank + 1:<5}\t{score:<20.12f}\t{rollno}\n")

    reader.close()

if __name__ == "__main__":
    index_path = sys.argv[1]
    query_file_path = sys.argv[2]
    output_file_path = sys.argv[3]
    rollno = sys.argv[4]
    search_index(index_path, query_file_path, output_file_path, rollno)