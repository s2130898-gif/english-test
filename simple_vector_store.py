"""
シンプルなベクトルストア（English Quiz System専用）
"""
import os
import json
import numpy as np
from typing import List, Dict
from simple_embeddings import SimpleEmbeddings

class SimpleVectorStore:
    def __init__(self, storage_path="quiz_vector_store.json"):
        self.storage_path = storage_path
        self.encoder = SimpleEmbeddings()
        self.documents = []
        self.load_documents()
        print(f"ベクトルストアを初期化しました (保存先: {self.storage_path})")

    def add_documents(self, documents: List[Dict[str, str]]):
        for doc in documents:
            embedding = self.encoder.encode_single(doc["text"])

            doc_with_embedding = {
                "id": doc["id"],
                "text": doc["text"],
                "metadata": doc.get("metadata", {}),
                "embedding": embedding
            }

            self.documents.append(doc_with_embedding)

        self.save_documents()
        print(f"{len(documents)}件のドキュメントを追加しました")

    def search(self, query: str, n_results: int = 5) -> List[Dict]:
        if not self.documents:
            return []

        query_embedding = self.encoder.encode_single(query)

        results = []
        for doc in self.documents:
            similarity = self.cosine_similarity(query_embedding, doc["embedding"])

            results.append({
                "id": doc["id"],
                "text": doc["text"],
                "metadata": doc["metadata"],
                "distance": 1 - similarity
            })

        results.sort(key=lambda x: x["distance"])

        return results[:n_results]

    def cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)

        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0

        return dot_product / (norm1 * norm2)

    def get_all_documents(self) -> List[Dict]:
        return [{
            "id": doc["id"],
            "text": doc["text"],
            "metadata": doc["metadata"]
        } for doc in self.documents]

    def save_documents(self):
        try:
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(self.documents, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存エラー: {e}")

    def load_documents(self):
        try:
            if os.path.exists(self.storage_path):
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    self.documents = json.load(f)
                print(f"{len(self.documents)}件のドキュメントを読み込みました")
            else:
                print("新規ベクトルストアを作成します")
        except Exception as e:
            print(f"読み込みエラー: {e}")
            self.documents = []

    def delete_collection(self):
        self.documents = []
        if os.path.exists(self.storage_path):
            os.remove(self.storage_path)
        print("コレクションを削除しました")