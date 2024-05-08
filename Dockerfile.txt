FROM python:latest
# Use the official Python image
FROM python:latest
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt
CMD ["python3", "app.py"]