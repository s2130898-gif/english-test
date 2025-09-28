"""
TF-IDF ベースの軽量埋め込みモデル
メモリ効率が高く、Streamlit Cloud無料プランで動作
"""
import numpy as np
from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer

class SimpleEmbeddings:
    """TF-IDFを使った軽量埋め込みモデル"""

    def __init__(self):
        print("📦 軽量埋め込みモデルを初期化中...")
        self.vectorizer = TfidfVectorizer(
            max_features=384,
            ngram_range=(1, 2),
            analyzer='char',
            min_df=1
        )
        self.dimension = 384
        self.fitted = False
        print("✅ TF-IDF埋め込みモデル (384次元) を初期化しました")

    def encode(self, texts: List[str]) -> np.ndarray:
        if not self.fitted:
            self.vectorizer.fit(texts)
            self.fitted = True

        embeddings = self.vectorizer.transform(texts).toarray()

        if embeddings.shape[1] < self.dimension:
            padding = np.zeros((embeddings.shape[0], self.dimension - embeddings.shape[1]))
            embeddings = np.hstack([embeddings, padding])
        elif embeddings.shape[1] > self.dimension:
            embeddings = embeddings[:, :self.dimension]

        return embeddings

    def encode_single(self, text: str) -> List[float]:
        return self.encode([text])[0].tolist()
