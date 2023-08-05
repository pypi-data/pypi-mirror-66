from setuptools import setup, find_packages
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pvqa',
    version ='0.0.2.1',
    author="PlantVillage",
    description="Question Answering System for Plants",
    long_description_content_type="text/markdown",
    keywords="plants question answering natural language processing deep learning cassava",
    packages=find_packages(),
    install_requires=["Flask==1.1.1",
                    "flask_cors==3.0.8",
                    "joblib==0.13.2",
                    "pandas==0.25.0",
                    "prettytable==0.7.2",
                    "transformers==2.1.1",
                    "scikit_learn==0.21.2",
                    "tika==1.19",
                    "torch==1.2.0",
                    "markdown==3.1.1",
                    "tqdm==4.32.2",
                    "wget==3.2", ]
)
