
  """
  軽量版埋め込みモデル（transformersのみ使用）
  """
  import numpy as np
  from typing import List
  from transformers import AutoTokenizer, AutoModel
  import torch

  class SimpleEmbeddings:
      def __init__(self):
          print("📦 軽量AI埋め込みモデルをロード中...")

          # より軽量なモデルを使用
          model_name = 'distilbert-base-uncased'  # 英語版（軽量）

          try:
              self.tokenizer = AutoTokenizer.from_pretrained(model_name)
              self.model = AutoModel.from_pretrained(model_name)
              self.model.eval()
              self.dimension = 768
              print(f"✅ {model_name} をロードしました")
          except Exception as e:
              print(f"エラー: {e}")
              # さらに軽量なフォールバック
              self.tokenizer = None
              self.model = None
              self.dimension = 100

      def encode(self, texts: List[str]) -> np.ndarray:
          if self.model is None:
              # フォールバック：ランダムベクトル
              return np.random.rand(len(texts), self.dimension)

          embeddings = []

          with torch.no_grad():
              for text in texts:
                  try:
                      inputs = self.tokenizer(
                          text,
                          return_tensors='pt',
                          truncation=True,
                          max_length=128,  # さらに短く
                          padding=True
                      )

                      outputs = self.model(**inputs)
                      # シンプルにCLSトークンのみ使用
                      embedding = outputs.last_hidden_state[:, 0, :].squeeze().numpy()
                      embeddings.append(embedding)
                  except:
                      # エラー時のフォールバック
                      embeddings.append(np.random.rand(self.dimension))

          return np.array(embeddings)

      def encode_single(self, text: str) -> List[float]:
          return self.encode([text])[0].tolist()
