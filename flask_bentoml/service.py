import os

os.environ["TRANSFORMERS_CACHE"] = "../model"

from transformers import pipeline


# 使用加载的模型和tokenizer创建一个pipeline
classifier = pipeline("sentiment-analysis")


def predict(text):
    """
    进行预测的函数，接收文本并返回预测结果。
    """
    result = classifier(text)
    return result
