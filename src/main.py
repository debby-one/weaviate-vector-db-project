import weaviate
from weaviate.connect import ConnectionParams
from weaviate.classes.init import AdditionalConfig, Timeout, Auth
import os

print("Hello, World!")

client = weaviate.WeaviateClient(
    connection_params=ConnectionParams.from_params(
        http_host="localhost",
        http_port=8099,
        http_secure=False,
        grpc_host="localhost",
        grpc_port=50052,
        grpc_secure=False,
    ),
    auth_client_secret=Auth.api_key("secr3tk3y"),
    additional_headers={
        "X-OpenAI-Api-Key": os.getenv("OPENAI_APIKEY")
    },
    additional_config=AdditionalConfig(
        timeout=Timeout(init=30, query=60, insert=120),  # Values in seconds
    ),
    skip_init_checks=False
)

client.connect()

# データを格納
data_object = {
    "name": "Sample Object",
    "description": "This is a sample description."
}

# データをExampleClassに追加
client.data_object.create(data_object, "ExampleClass")