FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
ENV PYTHONUNBUFFERED=1

# Use Gunicorn to serve the app (replace 'app:app' with your actual module if different)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "api:app"]
