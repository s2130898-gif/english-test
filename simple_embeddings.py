  """
  日本語対応Sentence-BERTモデル
  """
  import numpy as np
  from typing import List
  from sentence_transformers import SentenceTransformer

  class SimpleEmbeddings:
      """日本語対応のSentence-BERTモデル"""

      def __init__(self):
          print("📦 日本語対応AI埋め込みモデルをロード中...")
          print("⚠️ 初回起動時は3-4分かかります...")

          # 日本語に特化したモデル
          model_name = 'sonoisa/sentence-bert-base-ja-mean-tokens-v2'
          self.model = SentenceTransformer(model_name)

          self.dimension = 768
          print("✅ 日本語特化Sentence-BERTモデルをロードしました")
          print("🤖 ディープラーニングによるAI採点が有効です")

      def encode(self, texts: List[str]) -> np.ndarray:
          return self.model.encode(texts)

      def encode_single(self, text: str) -> List[float]:
          return self.model.encode([text])[0].tolist()
