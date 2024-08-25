# bentoml_build  
调用了huggingface上的一个情感分析的模型，集成到bento里，并容器化部署到docker上。  
使用Prometheus对页面的请求次数和预测次数进行监控  
  
## 运行flask服务  
```Bash
python app.py
```
![image](https://github.com/user-attachments/assets/4bda1f8d-405f-406d-8126-e6e8729e1df1)

## 构建和运行 Bento  
```Bash
bentoml build
bentoml serve app:svc
```
![image](https://github.com/user-attachments/assets/0f12539a-e116-4952-97b2-e245789c24fd)
![image](https://github.com/user-attachments/assets/59021138-96fc-4488-bc82-95137b815672)

## 容器化 Bento  
```Bash
 bentoml containerize sentiment_analysis_service:v6lu4ddcrknr4xb2
```
## 在本地运行 Docker 镜像
```Bash
docker run --rm -p 3000:3000 sentiment_analysis_service:v6lu4ddcrknr4xb2
```
## 运行Prometheus
![image](https://github.com/user-attachments/assets/d73cea36-cb02-49f0-9d7b-49ebc811bc3b)

## 运行grafana  
监控页面请求次数和预测次数
![image](https://github.com/user-attachments/assets/5028916c-6f11-4b2f-8221-07a6d6db30de)

