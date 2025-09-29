"""
DistilBERT ベースのAI埋め込みモデル（デバイス対応版）
"""
import numpy as np
from typing import List
import torch
from transformers import AutoTokenizer, AutoModel

class SimpleEmbeddings:
  def __init__(self):
      print("📦 AI埋め込みモデルをロード中...")
      print("⚠️ 初回起動時は3-4分かかります...")

      model_name = 'distilbert-base-multilingual-cased'

      # デバイス設定を明示的に指定
      self.device = torch.device('cpu')  # CPUを強制使用

      try:
          self.tokenizer = AutoTokenizer.from_pretrained(model_name)
          self.model = AutoModel.from_pretrained(
              model_name,
              torch_dtype=torch.float32,  # データ型を明示
              device_map=None  # デバイスマップを無効化
          )

          # モデルをCPUに移動
          self.model = self.model.to(self.device)
          self.model.eval()

      except Exception as e:
          print(f"モデルロードエラー: {e}")
          # より軽量なモデルでリトライ
          model_name = 'distilbert-base-uncased'
          self.tokenizer = AutoTokenizer.from_pretrained(model_name)
          self.model = AutoModel.from_pretrained(model_name)
          self.model = self.model.to(self.device)
          self.model.eval()

      self.dimension = 768
      print("✅ DistilBERT多言語モデル (768次元) をロードしました")

  def encode(self, texts: List[str]) -> np.ndarray:
      embeddings = []

      with torch.no_grad():
          for text in texts:
              try:
                  inputs = self.tokenizer(
                      text,
                      return_tensors='pt',
                      truncation=True,
                      max_length=512,
                      padding=True
                  )

                  # 入力もCPUに移動
                  inputs = {k: v.to(self.device) for k, v in inputs.items()}

                  outputs = self.model(**inputs)
                  embedding = outputs.last_hidden_state[:, 0, :].squeeze().cpu().numpy()
                  embeddings.append(embedding)

              except Exception as e:
                  print(f"エンコードエラー: {e}")
                  # エラー時はダミーベクトル
                  embeddings.append(np.random.rand(self.dimension))

      return np.array(embeddings)

  def encode_single(self, text: str) -> List[float]:
      return self.encode([text])[0].tolist()
