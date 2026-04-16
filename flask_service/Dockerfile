FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir flask
COPY . .
ENV FLASK_ENV=development
EXPOSE 5000
CMD ["python", "app.py"]