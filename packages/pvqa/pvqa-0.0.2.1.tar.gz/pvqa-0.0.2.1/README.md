# pvqa: Closed Domain Question Answering

QA System built on the HuggingFace Transformers library, for usage on the PlantVillage app.

## Table of Contents <!-- omit in toc -->

- [Installation](#Installation)
- [Getting started](#Getting-started)
  - [Preparing your data](#Preparing-your-data)
    - [Manual](#Manual)
    - [With converters](#With-converters)
  - [Downloading pre-trained models](#Downloading-pre-trained-models)
  - [Training models](#Training-models)
  - [Making predictions](#Making-predictions)
  - [Evaluating models](#Evaluating-models)
- [Notebook Examples](#Notebook-Examples)
- [Deployment](#Deployment)
  - [Manual](#Manual-1)
- [Contributing](#Contributing)
- [References](#References)
- [LICENSE](#LICENSE)

## Installation

### With pip

```shell
pip install pvqa
```

### From source

```shell
git clone https://github.com/PlantVillage/pvqa.git
cd pvqa/src
pip install -r requirements.txt
```

## Getting started

### Preparing your data

#### Manual

To use `pvqa` you need to create a pandas dataframe with the following columns:

| title             | paragraphs                                             |
| ----------------- | ------------------------------------------------------ |
| The Article Title | [Paragraph 1 of Article, ... , Paragraph N of Article] |

#### With converters

The objective of `pvqa` converters is to make it easy to create this dataframe from your raw documents database. For instance the `pdf_converter` can create a `pvqa` dataframe from a directory containing `.pdf` files:

```python
from pvqa.utils.converters import pdf_converter

df = pdf_converter(directory_path='path_to_pdf_folder')
```

You will need to install [Java OpenJDK](https://openjdk.java.net/install/) to use this converter. 

### Downloading pre-trained models and data

You can download the models from S3 or use the download functions:

```python
from pvqa.utils.download import download_squad, download_model

directory = 'path-to-directory'

# Downloading data
download_squad(dir=directory)

# Downloading pre-trained BERT fine-tuned on SQuAD 1.1
download_model('bert-squad_1.1', dir=directory)

# Downloading pre-trained DistilBERT fine-tuned on SQuAD 1.1
download_model('distilbert-squad_1.1', dir=directory)
```

### Training models

**Option 1**: Fit the pipeline on your plant information corpus using the pre-trained reader:

```python
import pandas as pd
from ast import literal_eval
from pvqa.pipeline import QAPipeline

df = pd.read_csv('your-custom-corpus-here.csv', converters={'paragraphs': literal_eval})

pvqa_pipeline = QAPipeline(reader='bert_qa.joblib') # use 'distilbert_qa.joblib' for DistilBERT instead of BERT
pvqa_pipeline.fit_retriever(df=df)
```

**Option 2**: If you want to fine-tune the reader on your custom SQuAD-like annotated dataset used for whatever plant you picked:

```python
pvqa_pipeline = QAPipeline(reader='bert_qa.joblib') # use 'distilbert_qa.joblib' for DistilBERT instead of BERT
pvqa_pipeline.fit_reader('path-to-custom-squad-like-dataset.json')
```

*Important*: Save the reader model after fine-tuning:
```python
pvqa_pipeline.dump_reader('path-to-save-bert-reader.joblib')
```
### Making predictions

To get the best prediction given an input query:

```python
pvqa_pipeline.predict(query='your question')
```

To get the N best predictions:
```python
pvqa_pipeline.predict(query='your question', n_predictions=N)
```

There is also the possibility to change the weight of the retriever score
versus the reader score in the computation of final ranking score (the default is 0.35, which is shown to be the best weight on the development set of SQuAD 1.1-open)

```python
pvqa_pipeline.predict(query='your question', retriever_score_weight=0.35)
```

Thanks to NVIDIA for the above functionality of retriever score weight.

### Evaluating models

In order to evaluate models on your custom plant compendium dataset you will need to annotate it! The annotation process can be done in 3 steps:

1. Convert your pandas DataFrame into a json file with SQuAD format:

    ```python
    from pvqa.utils.converters import df2squad

    json_data = df2squad(df=df, squad_version='v1.1', output_dir='.', filename='dataset-name')
    ```

2. Use an annotator to add ground truth question-answer pairs:

    Go to our [annotator](https://github.com/PlantVillage/pvqa/tree/dev/annotator) to easily annotate using SQuAD format.

3. Evaluate the pipeline object:

    ```python
    from pvqa.utils.evaluation import evaluate_pipeline

    evaluate_pipeline(pvqa_pipeline, 'path-to-annotated-dataset.json')

    ```

4. Evaluate the reader:

    ```python
    from pvqa.utils.evaluation import evaluate_reader

    evaluate_reader(pvqa_pipeline, 'path-to-annotated-dataset.json')
    ```

## Notebook Examples

Check the root directory for examples.

## Deployment

You can deploy a `pvqa` REST API by executing:

```shell
export dataset_path=path-to-dataset.csv
export reader_path=path-to-reader-model

FLASK_APP=api.py flask run -h 0.0.0.0
```

Make a request as follows:

```shell
http localhost:5000/api query=='your question here'
```

## UI 

We now have an available demo UI [here].
