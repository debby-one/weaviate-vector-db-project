import weaviate
from weaviate.classes.config import ReferenceProperty

def define_reference():
    """
    Create a Weaviate reference.
    """
    try:
        weaviate_client = weaviate.connect_to_custom(
            http_host="192.168.1.8",    # URL only, no http prefix
            http_port=8080,             # Default is 8080
            http_secure=False,          # Set to True if https
            grpc_host="192.168.1.8",    # URL only, no http prefix
            grpc_port=30021,            # Default is 50051, WCD uses 443
            grpc_secure=False,          # Edit as needed
            skip_init_checks=True,      # Set to True if you want to skip init checks
        )

        TestReport = weaviate_client.collections.get('TestReport')

        try:
            TestReport.config.add_reference(
                ReferenceProperty(
                    name='children',
                    target_collection='TestAnalysis'
                )
            )
        except Exception as e:
            print(f"エラーが発生しました。{e}")
    finally:
        weaviate_client.close()

if __name__ == "__main__":
    define_reference()