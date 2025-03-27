import weaviate

class WeaviateClient:
    def __init__(self, url, api_key=None):
        self.client = weaviate.Client(url=url, auth_client_secret=api_key)

    def create_object(self, class_name, properties):
        return self.client.data_object.create(properties, class_name)

    def get_object(self, class_name, object_id):
        return self.client.data_object.get(object_id, class_name)

    def update_object(self, class_name, object_id, properties):
        return self.client.data_object.update(object_id, properties, class_name)

    def delete_object(self, class_name, object_id):
        return self.client.data_object.delete(object_id, class_name)

    def query(self, query_string):
        return self.client.query.raw(query_string)