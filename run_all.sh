#!/bin/bash

# Indexing documents
echo "Indexing documents..."
python3 mtc23CS2311-indexer.py trec678rb/documents/ index/

# Searching indexed documents
echo "Searching indexed documents..."
python3 mtc23CS2311-searcher.py index/ trec678rb/topics/trec678.xml mtc23CS2311-output.txt CS2316

# Evaluating search results with the second relevance judgments file
echo "Evaluating search results with the second relevance judgments file..."
trec_eval/trec_eval -q trec678rb/qrels/trec678_301-450.qrel mtc23CS2311-output.txt > mtc23CS2311-eval.txt

echo "Process completed."

