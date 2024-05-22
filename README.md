# TREC Robust Indexing and Searching

This repository contains scripts for indexing and searching the TREC Robust document collection using the Whoosh library. The results are evaluated using the `trec_eval` tool.

## Prerequisites

- Python 3.x
- Whoosh library
- `trec_eval` tool
- A virtual environment (optional but recommended)

## Directory Structure
IR
├── index/ 
├── trec678rb/
│ ├── documents/
│ ├── qrels/
│ │ ├── robust_601-700.qrel
│ │ └── trec678_301-450.qrel
│ ├── topics/
│ │ ├── robust.xml
│ │ └── trec678.xml
├── mtc23CS2311-indexer.py
├── mtc23CS2311-searcher.py
├── mtc23CS2311-output.txt
├── mtc23CS2311-eval.txt
├── run_all.sh
└── test.py



## Setup

1. **Clone the repository** and navigate to the project directory.

2. **Create and activate a virtual environment** (optional but recommended):

    python3 -m venv /path/to/your/venv
    source /path/to/your/venv/bin/activate


3. **Install the required libraries**:

    pip install whoosh


4. **Clone the `trec_eval` tool**:

    git clone https://github.com/usnistgov/trec_eval
    cd trec_eval
    make
    cd ..


## Running the Scripts

### 1. Indexing the Documents

Activate your virtual environment if you haven't already:

    source /home/jasmine/data/pylucene_env/bin/activate


Run the indexing script:

    python3 mtc23CS2311-indexer.py trec678rb/documents/ index/

### 2. Searching the Indexed Documents

Run the searching script:

    python3 mtc23CS2311-searcher.py index/ trec678rb/topics/ mtc23CS2311-output.txt


### 3. Evaluating the Search Results

Run the `trec_eval` command to evaluate the search results:

    trec_eval/trec_eval -q trec678rb/qrels/trec678_301-450.qrel mtc23CS2311-output.txt > mtc23CS2311-eval.txt


## Files

- **mtc23CS2311-indexer.py**: Script to index the TREC Robust document collection.
- **mtc23CS2311-searcher.py**: Script to search the indexed documents using queries from a TREC Robust query file.
- **mtc23CS2311-output.txt**: Contains the search results in TREC format.
- **mtc23CS2311-eval.txt**: Contains the evaluation results.
- **test.py**: Script to test individual components of your scripts.


