import os
import wget
import boto3

def download_squad(dir="."):
    """
    Download SQuAD 1.1 and SQuAD 2.0 datasets

    Parameters
    ----------
    dir: str
        Directory where the dataset will be stored

    """

    dir = os.path.expanduser(dir)
    if not os.path.exists(dir):
        os.makedirs(dir)

    # Download SQuAD 1.1
    print("Downloading SQuAD v1.1 data...")

    dir_squad11 = os.path.join(dir, "SQuAD_1.1")
    squad11_urls = [
        "https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v1.1.json",
        "https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v1.1.json",
    ]

    if not os.path.exists(dir_squad11):
        os.makedirs(dir_squad11)

    for squad_url in squad11_urls:
        file = squad_url.split("/")[-1]
        if os.path.exists(os.path.join(dir_squad11, file)):
            print(file, "already downloaded")
        else:
            wget.download(url=squad_url, out=dir_squad11)

    # Download SQuAD 2.0
    print("\nDownloading SQuAD v2.0 data...")

    dir_squad20 = os.path.join(dir, "SQuAD_2.0")
    squad20_urls = [
        "https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v2.0.json",
        "https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v2.0.json",
    ]

    if not os.path.exists(dir_squad20):
        os.makedirs(dir_squad20)

    for squad_url in squad20_urls:
        file = squad_url.split("/")[-1]
        if os.path.exists(os.path.join(dir_squad20, file)):
            print(file, "already downloaded")
        else:
            wget.download(url=squad_url, out=dir_squad20)



def download_model(model, dir):
    """
    Downloads models from AWS S3 Bucket 'pv-qa' (either BERT or DistillBERT)

    Parameters
    ----------
    model: str 
        pick either 'bert-squad_1.1' or 'distilbert-squad_1.1'
    dir: str
        Directory where the dataset will be stored

    """
    s3 = boto3.resource('s3')
    BUCKET_NAME = 'pv-qa'
    if model == 'bert-squad_1.1':
        KEY = 'model-storage/bert_qa.joblib' 
        s3.Bucket(BUCKET_NAME).download_file(KEY, 'bert_qa.joblib')
    elif model == 'distilbert-squad_1.1':
        KEY = 'model-storage/distilbert_qa.joblib' 
        s3.Bucket(BUCKET_NAME).download_file(KEY, 'distilbert_qa.joblib') 
