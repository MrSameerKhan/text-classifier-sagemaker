from transformers import pipeline

# Download & cache the DistilBERT classifier
classifier = pipeline(
    "text-classification",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)
classifier.save_pretrained("./model")
print("Model downloaded to ./model")
