import weaviate
from weaviate.classes.query import QueryReference

def get_weaviate_data():
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

        print('parent object')
        for obj in TestReport.iterator(
            return_references=QueryReference(
                link_on='children',
                return_properties=["uuid"])
        ):
            print(obj.uuid)
            print('properties',obj.properties)
            for r in obj.references['children'].objects:
                print('reference uuid:',r.uuid)
            print('--------')

        print('children objects')
        for obj in TestAnalysis.iterator(
            return_references=QueryReference(
                link_on='parent',
                return_properties=["uuid"])
        ):
            print(obj.uuid)
            print('properties',obj.properties)
            for r in obj.references['parent'].objects:
                print('reference uuid:',r.uuid)
            print('--------')

    finally:
        weaviate_client.close()

if __name__ == "__main__":
    get_weaviate_data()