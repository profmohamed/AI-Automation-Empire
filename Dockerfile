FROM python:3.11-slim
WORKDIR /app
COPY python-core/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY python-core/ .
EXPOSE 8000
CMD ["python", "main.py"]
