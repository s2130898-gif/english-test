"""
シンプルな埋め込みモデル
"""
import os
import numpy as np
from typing import List
import hashlib

class SimpleEmbeddings:
    """シンプルな埋め込みモデル（デモ用）"""

    def __init__(self):
        self.dimension = 384
        print("シンプル埋め込みモデルを初期化しました")

    def encode(self, texts: List[str]) -> np.ndarray:
        embeddings = []

        for text in texts:
            text_hash = hashlib.md5(text.encode()).hexdigest()

            vector = []
            for i in range(0, len(text_hash), 2):
                value = int(text_hash[i:i+2], 16) / 255.0
                vector.append(value)

            while len(vector) < self.dimension:
                vector.extend(vector[:min(len(vector), self.dimension - len(vector))])

            vector = vector[:self.dimension]
            embeddings.append(vector)

        return np.array(embeddings)

    def encode_single(self, text: str) -> List[float]:
        return self.encode([text])[0].tolist()