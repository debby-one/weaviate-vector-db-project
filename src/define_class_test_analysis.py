import weaviate
import weaviate.classes.config as wc

def define_class_test_analysis():
    """
    Create a Weaviate class.
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

        weaviate_client.collections.create(
            name='TestAnalysis',
            properties=[wc.Property(name='chapter',data_type=wc.DataType.INT),
                        wc.Property(name='text',data_type=wc.DataType.TEXT)],
            references=[wc.ReferenceProperty(
                    name='parent',
                    target_collection='TestReport',
            )        
            ],
            vectorizer_config=[wc.Configure.NamedVectors.text2vec_weaviate(
                name='textdocument_vector',
                vectorize_collection_name=False,
            )        
            ]
        )

    finally:
        weaviate_client.close()

if __name__ == "__main__":
    define_class_test_analysis()