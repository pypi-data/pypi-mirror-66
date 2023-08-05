import pytest
from ast import literal_eval
import pandas as pd
import torch

from pvqa.utils.filters import filter_paragraphs
from pvqa.utils.download import *
from pvqa.pipeline import QAPipeline

def execute_pipeline(model, query, n_predictions=None):
    download_model(model + "-squad_1.1", dir="./models")
    df = pd.read_csv(
        "./data/cassava-v1.1.csv",
        converters={"paragraphs": literal_eval},
    )
    df = filter_paragraphs(df)

    reader_path = "models/" + model + "_qa.joblib"

    pvqa_pipeline = QAPipeline(reader=reader_path)
    pvqa_pipeline.fit_retriever(df)

    if n_predictions is not None:
        predictions = pvqa_pipeline.predict(query, n_predictions=n_predictions)
        result = []

        for answer, title, paragraph, score in predictions:
            prediction = (answer, title)
            result.append(prediction)
        return result
    else:
        prediction = pvqa_pipeline.predict(query)
        result = (prediction[0], prediction[1])
        return result

@pytest.mark.parametrize("model", ["bert", "distilbert"])
def test_predict(model):
    assert execute_pipeline(model,
        "What are major diseases affecting cassava?"
    ) == ("African Cassava Mosaic Virus, Cassava Bacterial Blight, Cassava Anthracnose Disease and Root Rot", "Cassava")


def test_n_predictions():
    predictions = execute_pipeline("distilbert",
        "What are major diseases affecting cassava?", 5
    )

    assert len(predictions) == 5

    assert predictions[0] == (
        "African Cassava Mosaic Virus, Cassava Bacterial Blight, Cassava Anthracnose Disease and Root Rot",
        "Cassava",
    )