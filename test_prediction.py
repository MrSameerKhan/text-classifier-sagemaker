import boto3, json

runtime = boto3.client("sagemaker-runtime", region_name="ap-south-2")

resp = runtime.invoke_endpoint(
    EndpointName="text-classifier-endpoint",
    ContentType="application/json",
    Body=json.dumps({"text":"I love machine learning!"})
)
print("Prediction:", resp['Body'].read().decode())
