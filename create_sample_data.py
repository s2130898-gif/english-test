"""
サンプルデータを直接ベクトルストアに追加（PDF不要）
"""
from simple_vector_store import SimpleVectorStore

def create_sample_data():
    print("=" * 60)
    print("Creating sample data for English Quiz System...")
    print("=" * 60)

    sample_sentences = [
        ("Artificial intelligence is transforming the way we live and work.",
         "人工知能は私たちの生活と仕事のあり方を変えています。"),
        ("Machine learning algorithms can identify patterns in large datasets.",
         "機械学習アルゴリズムは大規模なデータセットのパターンを識別できます。"),
        ("Natural language processing enables computers to understand human language.",
         "自然言語処理により、コンピュータが人間の言語を理解できます。"),
        ("Deep learning models require large amounts of training data to achieve high accuracy.",
         "ディープラーニングモデルは高精度を達成するために大量の訓練データを必要とします。"),
        ("Computer vision technology can recognize objects and faces in images.",
         "コンピュータビジョン技術は画像内の物体や顔を認識できます。"),
        ("Robotics combines mechanical engineering with artificial intelligence.",
         "ロボット工学は機械工学と人工知能を組み合わせたものです。"),
        ("Cloud computing provides scalable resources for data processing and storage.",
         "クラウドコンピューティングはデータ処理とストレージのためのスケーラブルなリソースを提供します。"),
        ("Cybersecurity is essential to protect sensitive information from unauthorized access.",
         "サイバーセキュリティは機密情報を不正アクセスから保護するために不可欠です。"),
        ("Blockchain technology ensures transparency and security in digital transactions.",
         "ブロックチェーン技術はデジタル取引の透明性とセキュリティを保証します。"),
        ("The Internet of Things connects everyday devices to the internet for smart automation.",
         "モノのインターネットは日常のデバイスをインターネットに接続してスマート自動化を実現します。"),
        ("Data analytics helps businesses make informed decisions based on trends and insights.",
         "データ分析は企業がトレンドと洞察に基づいて情報に基づいた意思決定を行うのを支援します。"),
        ("Virtual reality creates immersive experiences for entertainment and training purposes.",
         "バーチャルリアリティはエンターテインメントとトレーニングのための没入型体験を作り出します。"),
        ("Quantum computing has the potential to solve complex problems faster than classical computers.",
         "量子コンピューティングは古典的なコンピュータよりも速く複雑な問題を解決する可能性があります。"),
        ("Software development involves designing, coding, testing, and maintaining applications.",
         "ソフトウェア開発はアプリケーションの設計、コーディング、テスト、保守を含みます。"),
        ("Open source software allows developers to collaborate and improve code collectively.",
         "オープンソースソフトウェアは開発者が共同でコードを改善することを可能にします。"),
        ("The digital transformation is reshaping industries across the globe.",
         "デジタルトランスフォーメーションは世界中の産業を再構築しています。"),
        ("Big data technologies enable organizations to process massive volumes of information efficiently.",
         "ビッグデータ技術により、組織は膨大な量の情報を効率的に処理できます。"),
        ("Edge computing brings data processing closer to the source for faster response times.",
         "エッジコンピューティングはデータ処理をソースに近づけて応答時間を短縮します。"),
        ("Augmented reality overlays digital information onto the physical world.",
         "拡張現実は物理世界にデジタル情報を重ね合わせます。"),
        ("5G networks provide ultra-fast connectivity for mobile and IoT devices.",
         "5GネットワークはモバイルおよびIoTデバイスに超高速接続を提供します。"),
        ("Automation reduces manual tasks and increases operational efficiency.",
         "自動化は手動タスクを削減し、業務効率を向上させます。"),
        ("Neural networks mimic the structure of the human brain to process information.",
         "ニューラルネットワークは人間の脳の構造を模倣して情報を処理します。"),
        ("DevOps practices integrate development and operations for continuous delivery.",
         "DevOpsプラクティスは開発と運用を統合して継続的デリバリーを実現します。"),
        ("API integration allows different software systems to communicate seamlessly.",
         "API統合により、異なるソフトウェアシステムがシームレスに通信できます。"),
        ("Digital twins create virtual replicas of physical assets for simulation and analysis.",
         "デジタルツインは物理資産の仮想レプリカを作成してシミュレーションと分析を行います。"),
        ("Containerization technology simplifies application deployment across different environments.",
         "コンテナ化技術は異なる環境でのアプリケーション展開を簡素化します。"),
        ("Predictive analytics uses historical data to forecast future trends and behaviors.",
         "予測分析は過去のデータを使用して将来のトレンドと行動を予測します。"),
        ("Zero-trust security architecture assumes no user or device should be trusted by default.",
         "ゼロトラストセキュリティアーキテクチャはデフォルトでユーザーやデバイスを信頼しないことを前提としています。"),
        ("Agile methodology promotes iterative development and continuous improvement.",
         "アジャイル手法は反復的な開発と継続的な改善を促進します。"),
        ("Microservices architecture breaks applications into independent, deployable services.",
         "マイクロサービスアーキテクチャはアプリケーションを独立したデプロイ可能なサービスに分割します。"),
        ("Version control systems track changes to code and enable team collaboration.",
         "バージョン管理システムはコードの変更を追跡しチームコラボレーションを可能にします。"),
        ("Serverless computing allows developers to run code without managing infrastructure.",
         "サーバーレスコンピューティングは開発者がインフラストラクチャを管理せずにコードを実行できるようにします。"),
        ("Encryption protects sensitive data by converting it into unreadable code.",
         "暗号化は機密データを読み取れないコードに変換することで保護します。"),
        ("Load balancing distributes network traffic across multiple servers for optimal performance.",
         "負荷分散はネットワークトラフィックを複数のサーバーに分散して最適なパフォーマンスを実現します。"),
        ("Continuous integration automatically tests and merges code changes frequently.",
         "継続的インテグレーションはコード変更を頻繁に自動的にテストおよびマージします。"),
        ("Data warehousing consolidates information from multiple sources for business intelligence.",
         "データウェアハウジングは複数のソースから情報を統合してビジネスインテリジェンスを実現します。"),
        ("Graph databases are optimized for storing and querying interconnected data.",
         "グラフデータベースは相互接続されたデータの保存とクエリに最適化されています。"),
        ("Reinforcement learning trains models through trial and error with reward feedback.",
         "強化学習は報酬フィードバックによる試行錯誤を通じてモデルを訓練します。"),
        ("Content delivery networks cache data at edge locations to reduce latency.",
         "コンテンツ配信ネットワークはエッジロケーションにデータをキャッシュして遅延を削減します。"),
        ("Sentiment analysis uses NLP to determine emotional tone in text data.",
         "感情分析はNLPを使用してテキストデータの感情的なトーンを判断します。"),
        ("Infrastructure as code manages and provisions resources through machine-readable files.",
         "コードとしてのインフラストラクチャは機械可読ファイルを通じてリソースを管理およびプロビジョニングします。"),
        ("Real-time data processing analyzes information as it is generated or received.",
         "リアルタイムデータ処理は生成または受信された情報を即座に分析します。"),
        ("Multi-factor authentication adds extra layers of security beyond passwords.",
         "多要素認証はパスワードを超えた追加のセキュリティレイヤーを追加します。"),
        ("Distributed systems spread computing tasks across multiple machines for reliability.",
         "分散システムは信頼性のために複数のマシンにコンピューティングタスクを分散させます。"),
        ("Image recognition technology identifies and classifies objects within digital images.",
         "画像認識技術はデジタル画像内の物体を識別および分類します。"),
        ("Business intelligence tools transform raw data into actionable insights.",
         "ビジネスインテリジェンスツールは生データを実用的な洞察に変換します。"),
        ("Progressive web apps provide app-like experiences through web browsers.",
         "プログレッシブウェブアプリはウェブブラウザを通じてアプリのような体験を提供します。"),
        ("Machine translation systems automatically convert text from one language to another.",
         "機械翻訳システムはテキストをある言語から別の言語へ自動的に変換します。"),
        ("Chatbots use artificial intelligence to simulate human conversation.",
         "チャットボットは人工知能を使用して人間の会話をシミュレートします。"),
        ("Data mining extracts valuable patterns and knowledge from large datasets.",
         "データマイニングは大規模なデータセットから価値あるパターンと知識を抽出します。"),
    ]

    vector_store = SimpleVectorStore()

    documents = []
    for i, (english, japanese) in enumerate(sample_sentences):
        text = f"EN: {english}\nJP: {japanese}"
        doc = {
            "id": f"sample_sentence_{i+1}",
            "text": text,
            "metadata": {
                "source": "built-in_samples",
                "chunk_index": i,
                "total_chunks": len(sample_sentences)
            }
        }
        documents.append(doc)

    vector_store.add_documents(documents)

    print("\n" + "=" * 60)
    print(f"SUCCESS: Created {len(documents)} sample sentences!")
    print("=" * 60)
    print("\nYou can now start the quiz system:")
    print("  - Run: start_quiz.bat")
    print("  - Or:  streamlit run streamlit_english_quiz.py")
    print("=" * 60)

if __name__ == "__main__":
    create_sample_data()