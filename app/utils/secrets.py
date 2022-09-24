import boto3
import json

client = boto3.client("secretsmanager")


def get_secret_value(name: str):
    response = client.get_secret_value(SecretId=name)
    return json.loads(response["SecretString"])
