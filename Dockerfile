FROM python:3.10-slim

WORKDIR /opt/program

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

COPY . .

ENV PORT=8080
EXPOSE 8080

CMD ["gunicorn", "--workers=2", "--bind=0.0.0.0:8080", "wsgi:app"]
