import weaviate
from weaviate.classes.query import Filter

def clear_all_data():
    """
    Clear all data from Weaviate.
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
        assert weaviate_client.is_live()

        TestReport   = weaviate_client.collections.get('TestReport')
        TestAnalysis = weaviate_client.collections.get('TestAnalysis')

        # 親オブジェクトをすべて削除
        responce = TestReport.query.fetch_objects()
        ids = [o.uuid for o in responce.objects]
        if ids:
            TestReport.data.delete_many(
                where=Filter.by_id().contains_any(ids)
            )

        # 子オブジェクトを全て削除
        responce = TestAnalysis.query.fetch_objects()
        ids = [o.uuid for o in responce.objects]
        if ids:
            TestAnalysis.data.delete_many(
                where=Filter.by_id().contains_any(ids)
            )

    finally:
        weaviate_client.close()

if __name__ == "__main__":
    clear_all_data()