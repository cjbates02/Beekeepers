FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
ENV PYTHONUNBUFFERED=1

# CMD ["gunicorn", "--bind", "0.0.0.0:5050", "app:app"]
CMD ["python", "app.py"]
