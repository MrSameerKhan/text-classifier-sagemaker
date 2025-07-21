import json
from transformers import pipeline

# Load the cached model
classifier = pipeline("text-classification", model="./model")

def predict(text: str):
    return classifier(text)

# SageMaker WSGI handler
def handler(environ, start_response):
    path = environ.get('PATH_INFO', '')
    if path == '/ping':
        start_response('200 OK', [('Content-Type','application/json')])
        return [b'{"status":"ok"}']
    if path == '/invocations':
        length = int(environ.get('CONTENT_LENGTH', 0))
        body = environ['wsgi.input'].read(length)
        data = json.loads(body)
        text = data.get("text","")
        result = predict(text)
        response = json.dumps(result).encode('utf-8')
        start_response('200 OK', [('Content-Type','application/json')])
        return [response]
    start_response('404 Not Found', [('Content-Type','application/json')])
    return [b'{"error":"Unsupported endpoint"}']
