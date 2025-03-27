import weaviate
import numpy as np

def preprocess_text(text):
    # テキストの前処理を行う関数
    text = text.lower().strip()
    return text

def vectorize_text(client, text):
    # Weaviateを使用してテキストをベクトル化する関数
    response = client.query.get("Text", ["vector"]).with_where({
        "path": ["text"],
        "operator": "Equal",
        "valueString": text
    }).do()
    
    if response and 'data' in response and 'Get' in response['data']:
        return response['data']['Get']['Text'][0]['vector']
    return None

def save_vectors_to_file(vectors, filename):
    # ベクトルをファイルに保存する関数
    np.save(filename, vectors)

def load_vectors_from_file(filename):
    # ファイルからベクトルを読み込む関数
    return np.load(filename)