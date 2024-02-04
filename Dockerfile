# 使用Python作为基础镜像
FROM python:3.9

# 设置工作目录
WORKDIR /app

# 安装Apache的开发包
RUN apt-get update && apt-get install -y apache2-dev

# 复制应用程序代码到容器中
COPY . /app/

# 创建和激活虚拟环境
RUN python -m venv /opt/venv
RUN . /opt/venv/bin/activate

# 安装Django应用程序的依赖项
RUN pip install -r requirements.txt
