import sqlite3
import utils
import bentoml
from bentoml.io import JSON
from flask import Flask, request, jsonify, render_template, g
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import psutil
import logging
import GPUtil
from prometheus_client import Counter, generate_latest, Gauge
from transformers_service import predict

# 定义 BentoML 服务
svc = bentoml.Service("sentiment_analysis_service")

# 创建 Flask 应用
app = Flask(__name__)

# 设置限流器
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["60 per minute", "2 per second"],
)

# 设置日志
logging.basicConfig(filename='logs/requests.log', level=logging.INFO)

# Prometheus 指标
REQUESTS = Counter('requests_total', 'Total number of requests')
PREDICTION_COUNT = Counter("prediction_count", "Total number of predictions made")
CPU_USAGE = Gauge('cpu_usage', 'CPU usage in percentage')
MEMORY_USAGE = Gauge('memory_usage', 'Memory usage in percentage')
GPU_MEMORY_TOTAL = Gauge('gpu_memory_total', 'Total GPU memory in MB', ['gpu_id'])
GPU_MEMORY_USED = Gauge('gpu_memory_used', 'Used GPU memory in MB', ['gpu_id'])
GPU_LOAD = Gauge('gpu_load', 'GPU load', ['gpu_id'])



@app.route("/", methods=["GET", "POST"])
@limiter.limit("60/minute; 2/second")
def index():
    REQUESTS.inc()
    result = None
    error_message = None
    if request.method == "POST":
        api_key = request.form["api_key"]
        text = request.form["text"]

        # 验证 API Key
        key_record = utils.get_key("sentiment-analysis")
        if key_record == api_key:
            PREDICTION_COUNT.inc()
            result = predict(text)
            # 记录日志
            logging.info(f"API Key: {api_key}, IP: {request.remote_addr}, Input: {text}, "
                         f"cpu_usage: {psutil.cpu_percent(interval=1)}, memory_usage: {psutil.virtual_memory()}")
            # 记录响应
            logging.info(f"Response: {result}")
        else:
            error_message = "Invalid API Key. Please try again."

    return render_template("index.html", result=result, error_message=error_message)


@app.route("/predict", methods=["POST"])
@limiter.limit("60/minute; 2/second")
def predict_route():
    REQUESTS.inc()
    data = request.get_json()
    api_key = data.get("api_key")
    text = data.get("text")

    # 验证 API Key
    key_record = utils.get_key("sentiment-analysis")
    if not key_record == api_key:
        return jsonify({"error": "Invalid API Key"}), 403

    # 增加预测计数
    PREDICTION_COUNT.inc()

    # 记录日志
    logging.info(f"API Key: {api_key}, IP: {request.remote_addr}, Input: {text}, "
                 f"cpu_usage: {psutil.cpu_percent(interval=1)}, memory_usage: {psutil.virtual_memory()}")

    # 进行预测
    result = predict(text)

    # 记录响应
    logging.info(f"Response: {result}")
    return jsonify(result)


def collect_system_metrics():
    """收集系统指标并更新到 Prometheus 中"""
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    gpu_info = GPUtil.getGPUs()

    CPU_USAGE.set(cpu_usage)
    MEMORY_USAGE.set(memory_info.percent)

    for gpu in gpu_info:
        GPU_MEMORY_TOTAL.labels(gpu_id=gpu.id).set(gpu.memoryTotal)
        GPU_MEMORY_USED.labels(gpu_id=gpu.id).set(gpu.memoryUsed)
        GPU_LOAD.labels(gpu_id=gpu.id).set(gpu.load)


@app.route("/metrics", methods=["GET"])
def metrics():
    collect_system_metrics()  # 在每次请求时更新系统指标
    return generate_latest()


@app.route("/system_metrics", methods=["GET"])
def system_metrics():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    gpu_info = GPUtil.getGPUs()

    gpu_usage = [{"id": gpu.id, "load": gpu.load, "memoryTotal": gpu.memoryTotal, "memoryUsed": gpu.memoryUsed} for gpu
                 in gpu_info]

    return jsonify({
        "cpu_usage": cpu_usage,
        "memory_total": memory_info.total,
        "memory_used": memory_info.used,
        "gpu_info": gpu_usage
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
