
  """
  日本語対応Sentence-BERTモデル（改善版）
  """
  import numpy as np
  from typing import List
  from sentence_transformers import SentenceTransformer
  import re

  class SimpleEmbeddings:
      def __init__(self):
          print("📦 日本語対応AI埋め込みモデルをロード中...")

          # より良い日本語モデルを使用
          model_name = 'pkshatech/GLuCoSE-base-ja'  # NTTの日本語特化モデル
          try:
              self.model = SentenceTransformer(model_name)
              print(f"✅ {model_name}をロードしました")
          except:
              # フォールバック
              model_name = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'
              self.model = SentenceTransformer(model_name)
              print(f"✅ {model_name}をロードしました")

          self.dimension = 768

      def preprocess_japanese(self, text: str) -> str:
          """日本語テキストの前処理"""
          # 助詞を削除（簡易版）
          particles = ['は', 'が', 'を', 'に', 'へ', 'と', 'から', 'まで', 'で', 'の']
          for p in particles:
              text = text.replace(p, ' ')
          # 連続するスペースを1つに
          text = re.sub(r'\s+', ' ', text)
          return text.strip()

      def encode(self, texts: List[str]) -> np.ndarray:
          # 前処理を適用
          processed_texts = [self.preprocess_japanese(t) for t in texts]
          return self.model.encode(processed_texts)

      def encode_single(self, text: str) -> List[float]:
          processed = self.preprocess_japanese(text)
          return self.model.encode([processed])[0].tolist()
