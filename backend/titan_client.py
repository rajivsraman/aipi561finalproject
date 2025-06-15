import boto3
import os
import json
import time

BEDROCK_REGION = os.getenv("AWS_REGION", "us-east-1")
MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "amazon.titan-tg1-large")
bedrock = boto3.client("bedrock-runtime", region_name=BEDROCK_REGION)

def query_titan(prompt: str) -> str:
    start = time.time()
    resp = bedrock.invoke_model(
        modelId=MODEL_ID,
        contentType="application/json",
        accept="application/json",
        body=json.dumps({"inputText": prompt})
    )
    latency = time.time() - start
    body = json.loads(resp["body"].read().decode())
    return body.get("results", [{}])[0].get("outputText", "No output.")