FROM python:3.10-slim-buster
WORKDIR /app
COPY . /app

# We are using this as we are trying to deploy it on AWS s3 cloud
# RUN apt update -y && apt install awscli -y  
CMD ["python3","app.py"]