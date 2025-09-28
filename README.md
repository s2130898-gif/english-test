# 🎓 English Quiz System（独立版）

RAGの検索機能を利用した英語学習システム。**完全に独立して動作**し、他のRAGシステムと依存関係はありません。

## ✨ 特徴

- ✅ **完全独立**: 他のRAGシステムとは別のデータベースを使用
- ✅ **簡単セットアップ**: ワンクリックで開始
- ✅ **50文収録**: 技術系英日対訳サンプル付き
- ✅ **高度な採点**: ベクトル類似度 + 単語一致率 + 文字列類似度
- ✅ **助詞除外**: 内容語のみで評価（より正確な採点）
- ✅ **詳細な分析**: 採点プロセスを完全可視化

## 📋 必要なもの

- **Python 3.7以上**
  - ダウンロード: https://www.python.org/downloads/
- **インターネット接続**（初回インストール時のみ）

## 🚀 Google Driveからインストール

### **方法1: 完全自動（推奨）**

1. フォルダをダウンロード
2. **`START_HERE.bat`** をダブルクリック

これだけです！自動的に：
- 必要なパッケージをインストール
- サンプルデータを作成
- クイズシステムを起動

### **方法2: 手動インストール**

1. **`install.bat`** をダブルクリック（パッケージインストール）
2. **`setup.bat`** をダブルクリック（サンプルデータ作成）
3. **`start_quiz.bat`** をダブルクリック（クイズ起動）

## 🚀 クイックスタート

### ステップ1: サンプルPDF作成
```
create_sample.bat をダブルクリック
```
→ `english_japanese_sample.pdf` が作成されます（50文収録）

### ステップ2: PDFをアップロード
```
start_uploader.bat をダブルクリック
```
1. ブラウザが開きます
2. 「PDFファイルを選択」をクリック
3. `english_japanese_sample.pdf` を選択
4. 「処理を開始」をクリック
5. 完了したらブラウザを閉じる

### ステップ3: クイズ開始
```
start_quiz.bat をダブルクリック
```
1. 「新しい問題を出題」をクリック
2. 英文を読んで和訳を入力
3. 「採点する」をクリック
4. スコアとフィードバックを確認

## 📁 ファイル構成

```
english-quiz-system/
├── start_uploader.bat           # PDFアップローダー起動
├── start_quiz.bat               # クイズシステム起動
├── create_sample.bat            # サンプルPDF作成
├── create_sample_pdf.py         # サンプルPDF生成スクリプト
├── english_quiz_system.py       # コアロジック
├── streamlit_english_quiz.py    # クイズGUI
├── streamlit_pdf_uploader.py    # アップロードGUI
├── pdf_uploader.py              # PDF処理ロジック
├── simple_vector_store.py       # ベクトルストア（独立）
├── simple_embeddings.py         # 埋め込みモデル
├── quiz_vector_store.json       # データベース（自動生成）
└── README.md                    # このファイル
```

## 🎯 使用例

### 1. 技術文書で学習
```python
# create_sample.bat を実行すると
# AI、機械学習、クラウドなどの技術文書50文が生成されます
```

### 2. 独自のPDFを使用
以下の形式でPDFを作成:
```
EN: Your English sentence here.
JP: 日本語訳をここに。

EN: Another sentence.
JP: 別の文章。
```

### 3. 採点システム
- **90点以上**: グレードS - 完璧！
- **80-89点**: グレードA - 素晴らしい
- **70-79点**: グレードB - 良い
- **60-69点**: グレードC - まずまず
- **40-59点**: グレードD - もう少し
- **40点未満**: グレードF - 要改善

## ⚙️ カスタマイズ

### 英文の長さを変更
`english_quiz_system.py` の Line 21:
```python
def extract_english_sentences(self, text, min_length=50, max_length=200):
    # min_length, max_length を変更
```

### チャンクサイズを変更
アップロード時のスライダーで調整可能（100-2000文字）

### 採点基準を変更
`english_quiz_system.py` の Line 56-68:
```python
if score >= 90:
    grade = 'S'
# 基準値を変更可能
```

## 🔧 トラブルシューティング

### Q: ドキュメントがありません
**A**: `start_uploader.bat` でPDFをアップロードしてください

### Q: 英文が見つかりません
**A**: PDFに英文が含まれているか確認してください

### Q: 採点スコアが低い
**A**: より多くのPDFを追加するか、英日対訳のあるPDFを使用してください

### Q: データをリセットしたい
**A**: `quiz_vector_store.json` を削除するか、アップローダーの「全データを削除」ボタンを使用

## 📊 データ管理

### バックアップ
```bash
# データファイルをコピー
copy quiz_vector_store.json quiz_vector_store_backup.json
```

### 復元
```bash
# バックアップから復元
copy quiz_vector_store_backup.json quiz_vector_store.json
```

### データ削除
```bash
# データファイルを削除
del quiz_vector_store.json
```

## 💡 Tips

- **学習効率UP**: 毎日10問ずつ挑戦
- **弱点克服**: スコアが低かった問題を記録して復習
- **語彙強化**: 様々な分野のPDFを追加
- **継続が鍵**: 学習統計で進捗を確認

## 🎓 収録内容（サンプルPDF）

- AI・機械学習（15文）
- クラウド・インフラ（10文）
- セキュリティ（5文）
- データ分析（8文）
- ソフトウェア開発（12文）

## 🔗 関連ファイル

- `streamlit_english_quiz.py` - メインクイズアプリ
- `streamlit_pdf_uploader.py` - PDFアップローダー
- `english_quiz_system.py` - CLI版（ターミナルで実行）

## 📝 ライセンス

このプロジェクトは独立したEnglish Quiz Systemです。
元のRAGシステムとは別のデータベースを使用します。