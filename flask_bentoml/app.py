import bentoml
from bentoml.io import JSON
from flask import Flask, request, jsonify, render_template, redirect
from prometheus_client import Counter, generate_latest
from service import predict

# 定义 BentoML 服务
svc = bentoml.Service("sentiment_analysis_service")

# 定义 Prometheus 指标
REQUESTS = Counter('requests_total', 'Total number of requests')
PREDICTION_COUNT = Counter("prediction_count", "Total number of predictions made")

# 创建 Flask 应用
app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    REQUESTS.inc()
    result = None
    if request.method == "POST":
        # 增加预测计数
        PREDICTION_COUNT.inc()
        text = request.form["text"]
        result = predict(text)
    return render_template("index.html", result=result)

@app.route("/predict", methods=["POST"])
def predict_route():
    data = request.get_json()
    text = data["text"]

    # 增加预测计数
    PREDICTION_COUNT.inc()

    # 使用 BentoML 服务进行预测
    result = predict(text)
    return jsonify(result)


@app.route("/metrics", methods=["GET"])
def metrics():
    return generate_latest()

# 如果作为BentoML服务运行
@svc.api(input=JSON(), output=JSON())
async def bentoml_predict(input_data):
    return predict(input_data["text"])

# 启动 Flask 应用
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
