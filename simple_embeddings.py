  """
  DistilBERT ベースのAI埋め込みモデル
  多言語対応（日本語・英語）のディープラーニングモデル
  """
  import numpy as np
  from typing import List
  import torch
  from transformers import AutoTokenizer, AutoModel

  class SimpleEmbeddings:
      """DistilBERTを使ったAI埋め込みモデル"""

      def __init__(self):
          print("📦 AI埋め込みモデルをロード中...")
          print("⚠️ 初回起動時は3-4分かかります...")

          model_name = 'distilbert-base-multilingual-cased'

          self.tokenizer = AutoTokenizer.from_pretrained(model_name)
          self.model = AutoModel.from_pretrained(model_name)

          self.model.eval()

          self.dimension = 768

          print("✅ DistilBERT多言語モデル (768次元) をロードしました")
          print("🤖 ディープラーニングによるAI採点が有効です")

      def encode(self, texts: List[str]) -> np.ndarray:
          embeddings = []

          with torch.no_grad():
              for text in texts:
                  inputs = self.tokenizer(
                      text,
                      return_tensors='pt',
                      truncation=True,
                      max_length=512,
                      padding=True
                  )

                  outputs = self.model(**inputs)

                  # Mean poolingを使用（改善版）
                  attention_mask = inputs['attention_mask']
                  hidden_states = outputs.last_hidden_state

                  masked_embeddings = hidden_states * attention_mask.unsqueeze(-1)
                  sum_embeddings = masked_embeddings.sum(dim=1)
                  sum_mask = attention_mask.sum(dim=1, keepdim=True)

                  embedding = (sum_embeddings / sum_mask.clamp(min=1e-9)).squeeze().numpy()

                  embeddings.append(embedding)

          return np.array(embeddings)

      def encode_single(self, text: str) -> List[float]:
          return self.encode([text])[0].tolist()
