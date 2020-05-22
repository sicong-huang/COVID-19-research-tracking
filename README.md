# A project to keep track of COVID-19 related research
This project takes an existing XML file in the [format provided by MIDAS](https://github.com/midas-network/COVID-19/tree/master/documents/mendeley_library_files/xml_files)
, analyze the articles in the XML and output them in groups.

## How it works
The central concept used in this project is latent dirichlet allocation (LDA). LDA transforms the bag-of-word representation of documents into probability distributions of topics. Because the xml file only provides abstracts instead of whole papers, only abstracts are used in the analysis.

Preprocessing is done by [scispacy](https://allenai.github.io/scispacy/), the [spacy](https://spacy.io) model trained on biomedical texts. In this step scispacy performs tokenization and stop-words removal. Whitespace characters and punctuations are also removed.  
This project uses the [gensim](https://radimrehurek.com/gensim/) implementation of LDA, which trains an LdaModel according to the number of topics specified (default 5).  
After assigning a topic to each document, a representative document is chosen for each topic. This process builds a graph for each topic, where documents are vertices. Edge weights are computed as the similarity between documents' topic distribution. The document with highest degree centrality is picked as the representative.

## Setup
Create a python 3.7 virtual environment. Activate the environment and run
```
pip install -r requirements.txt
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.2.4/en_core_sci_md-0.2.4.tar.gz
```

## Usage
The default run is as simple as running `main.py` without any arguments 
```
python main.py
```
By default, it uses `mendeley_document_library_2020-03-25.xml` in this repository as the input xml file. Also by default, output files are store in `groups/`, in which `grouping.txt` stores grouping information (i.e. topic number, number of documents in this topic, keywords, and representative document), and `group#.txt` stores the documents classified to that group.

Default run should generate commandline output as
```
$python main.py
reading from mendeley_document_library_2020-03-25.xml
found 1061 articles
100%|███████████████████████████████████████| 851/851 [00:41<00:00, 20.27it/s]
using 851 valid articles
training LDA
Finished training/loading
Topic coherence: -1.3018196273692855
Num of topics: 5
```
Once the program finish execution, corpus and model information is stored in `cache/` for faster loading; therefore, the next time when running with the same XML file, it loads from `cache` instead of building from stretch. You can force it read from XML or train a new model by passing arguments `--force_read` and `--force_train`.

Here is the help message
```
$python main.py --help
usage: main.py [-h] [--xml_file XML_FILE] [--out_dir OUT_DIR]
               [--num_topics NUM_TOPICS] [--force_read] [--force_train]

optional arguments:
  -h, --help            show this help message and exit
  --xml_file XML_FILE   path to the XML to read from
  --out_dir OUT_DIR     output directory
  --num_topics NUM_TOPICS
                        number of groups/topics to form
  --force_read          force to read from XML file
  --force_train         force to trian new model
  ```
