# bentoml_build  
调用了huggingface上的一个情感分析的模型，集成到bento里，并容器化部署到docker上。  
使用Prometheus对相关参数进行监控  
  
## 运行flask服务  
```Bash
python app.py
```
![image](https://github.com/user-attachments/assets/dc7564f6-b9c7-40b1-a8d3-93fc42d41e21)  
![image](https://github.com/user-attachments/assets/1ccb5821-f398-4d0c-9f50-6c615b5c0c1b)  



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
![image](https://github.com/user-attachments/assets/5441a915-607c-47a0-86b4-e8bcecb67b39)


## 记录的一些指标  
![image](https://github.com/user-attachments/assets/5cbd2a20-cd5a-4abb-a827-ab687f07450c)  

## 请求响应日志记录在requests.log文件中  
![image](https://github.com/user-attachments/assets/0b2bfcee-6cfb-4729-a7d0-2e143ade076e)
 

## 调用次数限制
![image](https://github.com/user-attachments/assets/7d542ca4-42a4-46b9-8f0b-518690062511)
![image](https://github.com/user-attachments/assets/de0c2c56-316f-4e79-ae13-8ed7920d7ec1)

## 一些问题  
1.我的电脑是amd的集显，GPU相关参数好像记录不到。
2.没有做到在创建模型的时候生成API-key记录到数据库中，目前是我用另外的方法生成10位随机的字符串并记录到数据库中的。

