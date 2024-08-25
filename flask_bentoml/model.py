import os

os.environ["TRANSFORMERS_CACHE"] = "../model"

import bentoml
from transformers import pipeline


classifier = pipeline("sentiment-analysis")
bento_model = bentoml.transformers.save_model("sentiment-analysis", classifier)

print(f"Model saved: {bento_model}")
