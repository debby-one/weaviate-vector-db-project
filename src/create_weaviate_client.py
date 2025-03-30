import weaviate
import os

def create_weaviate_client():
    """
    Create a Weaviate client instance.
    """
    try:
        api_key = os.getenv("WEAVIATE_APIKEY")
        weaviate_client = weaviate.connect_to_custom(
            http_host="192.168.1.8",    # URL only, no http prefix
            http_port=8080,             # Default is 8080
            http_secure=False,          # Set to True if https
            grpc_host="192.168.1.8",    # URL only, no http prefix
            grpc_port=30021,            # Default is 50051, WCD uses 443
            grpc_secure=False,          # Edit as needed
            skip_init_checks=True,      # Set to True if you want to skip init checks
            auth_credentials=None,
            headers={
                "Bearer": f"{api_key}"
            }
        )
        assert weaviate_client.is_live()

        TestReport   = weaviate_client.collections.get('TestReport')
        TestAnalysis = weaviate_client.collections.get('TestAnalysis')

        # TestReport(親オブジェクト)作成
        parentUUID = TestReport.data.insert({
            'title':"TestDocument1",
            'summary':"この文章はテストドキュメントです。"
        })
        print("parent object insert success:uuid=",parentUUID)

        sentences     = [1,2,3]
        texts         = ["目的","機能詳細","品質保証"]
        childrenUUIDs = []

        # TestAnalysis(子オブジェクト)作成
        with TestAnalysis.batch.dynamic() as batch:
            for chapter,text in zip(sentences,texts):
                uuid = batch.add_object(
                    properties={
                        'chapter': chapter,
                        'text': text
                    },
                    references={'parent':parentUUID}
                )
                childrenUUIDs.append(uuid)
                print("children uuid=",uuid)
        print("children object insert success")

        # TestReportに対して、TestAnalysisへのリファレンスをバッチ挿入する
        with TestReport.batch.dynamic() as batch:
            batch.add_reference(
                from_property='children',
                from_uuid=parentUUID,
                to=childrenUUIDs
            )
        print("adding reference of parent's obj success")

    finally:
        weaviate_client.close()

if __name__ == "__main__":
    create_weaviate_client()