import json
from ast import literal_eval
import pandas as pd
import torch

from pvqa.utils.filters import filter_paragraphs
from pvqa.utils.evaluation import evaluate_pipeline, evaluate_reader
from pvqa.utils.download import *
from pvqa.pipeline import QAPipeline


def test_evaluate_pipeline():

    download_model("bert-squad_1.1", dir="./models")
    df = pd.read_csv(
        "./data/cassava/cassava0.csv",
        converters={"paragraphs": literal_eval},
    )
    df = filter_paragraphs(df)

    test_data = {
        "data": [
            {
                "title": "Cassava plant",
                "paragraphs": [
                    {
                        "context": "Major diseases attacking cassava are African Cassava Mosaic Virus, Cassava Bacterial Blight, Cassava Anthracnose Disease and Root Rot. Mealybug, greenmite, termite and variegated grasshoppers are the major insect pests of cassava.",
                        "qas": [
                            {
                                "answers": [
                                    {"answer_start": 37, "text": "African Cassava Mosaic Virus, Cassava Bacterial Blight, Cassava Anthracnose Disease and Root Rot"},
                                    {"answer_start": 37, "text": "African Cassava Mosaic Virus, Cassava Bacterial Blight, Cassava Anthracnose Disease and Root Rot"},
                                    {"answer_start": 37, "text": "African Cassava Mosaic Virus, Cassava Bacterial Blight, Cassava Anthracnose Disease and Root Rot"},
                                ],
                                "question": "What are major diseases affecting cassava?",
                                "id": "56be4db4acb8001400a502ec",
                            }
                        ],
                    }
                ],
            }
        ],
        "version": "1.1",
    }

    with open("./test_data.json", "w") as f:
        json.dump(test_data, f)

    pvqa_pipeline = QAPipeline(reader="./models/bert_qa.joblib", n_jobs=-1)
    pvqa_pipeline.fit_retriever(df)

    eval_dict = evaluate_pipeline(pvqa_pipeline, "./test_data.json", output_dir=None)

    assert eval_dict["exact_match"] > 0.8
    assert eval_dict["f1"] > 0.8


def test_evaluate_reader():

    download_model("bert-squad_1.1", dir="./models")
    pvqa_pipeline = QAPipeline(reader="./models/bert_qa.joblib", n_jobs=-1)
    eval_dict = evaluate_reader(pvqa_pipeline, "./test_data.json")

    assert eval_dict["exact_match"] > 0.8
    assert eval_dict["f1"] > 0.8