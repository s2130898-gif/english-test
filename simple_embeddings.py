"""
Sentence Transformers ベースの埋め込みモデル
多言語対応（日本語・英語）
"""
import numpy as np
from typing import List
from sentence_transformers import SentenceTransformer

class SimpleEmbeddings:
    """Sentence Transformersを使った埋め込みモデル"""

    def __init__(self):
        print("📦 埋め込みモデルをロード中...")
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        self.dimension = 384
        print("✅ 多言語埋め込みモデル (384次元) をロードしました")

    def encode(self, texts: List[str]) -> np.ndarray:
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings

    def encode_single(self, text: str) -> List[float]:
        return self.encode([text])[0].tolist()