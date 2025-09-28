"""
English Quiz System using RAG
RAGシステムから英文を抽出し、和訳を採点するシステム
"""
import sys
import os
import re
import random
from difflib import SequenceMatcher
import numpy as np
from collections import Counter
from janome.tokenizer import Tokenizer

from simple_vector_store import SimpleVectorStore
from simple_embeddings import SimpleEmbeddings


class EnglishQuizSystem:
    def __init__(self):
        self.vector_store = SimpleVectorStore()
        self.embeddings = SimpleEmbeddings()
        self.tokenizer = Tokenizer()
        self.current_question = None
        self.score_history = []

    def extract_english_sentences(self, text, min_length=50, max_length=200):
        sentences = re.split(r'[.!?]\s+', text)

        english_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()

            if len(sentence) < min_length or len(sentence) > max_length:
                continue

            ascii_chars = sum(1 for c in sentence if ord(c) < 128)
            if ascii_chars / len(sentence) > 0.7:
                english_sentences.append(sentence)

        return english_sentences

    def get_random_english_question(self):
        all_docs = self.vector_store.get_all_documents()

        if not all_docs:
            return None

        random.shuffle(all_docs)

        for doc in all_docs:
            doc_text = doc['text']

            if 'EN:' in doc_text and 'JP:' in doc_text:
                lines = doc_text.split('\n')
                english_line = None
                japanese_line = None

                for line in lines:
                    if line.startswith('EN:'):
                        english_line = line.replace('EN:', '').strip()
                    elif line.startswith('JP:'):
                        japanese_line = line.replace('JP:', '').strip()

                if english_line and japanese_line:
                    self.current_question = {
                        'english': english_line,
                        'japanese': japanese_line,
                        'source': doc.get('metadata', {}).get('source', 'Unknown'),
                        'doc_id': doc['id']
                    }
                    return self.current_question
            else:
                sentences = self.extract_english_sentences(doc_text)
                if sentences:
                    selected_sentence = random.choice(sentences)
                    self.current_question = {
                        'english': selected_sentence,
                        'source': doc.get('metadata', {}).get('source', 'Unknown'),
                        'doc_id': doc['id']
                    }
                    return self.current_question

        return None

    def calculate_similarity(self, text1, text2):
        text1 = text1.lower().strip()
        text2 = text2.lower().strip()

        text1 = re.sub(r'[、。！？\s]+', '', text1)
        text2 = re.sub(r'[、。！？\s]+', '', text2)

        return SequenceMatcher(None, text1, text2).ratio()

    def tokenize_japanese(self, text):
        excluded_pos = {
            '助詞',
            '助動詞',
            '記号',
            '接続詞',
            '接頭詞',
            '非自立'
        }

        excluded_words = {
            'です', 'ます', 'である', 'だ', 'た', 'れる', 'られる',
            'せる', 'させる', 'ない', 'ぬ', 'う', 'よう'
        }

        words = []
        tokens = self.tokenizer.tokenize(text)

        for token in tokens:
            parts = token.split('\t')
            if len(parts) < 2:
                continue

            surface = parts[0]
            features = parts[1].split(',')

            if len(features) < 1:
                continue

            pos = features[0]

            is_excluded_pos = any(ex in pos for ex in excluded_pos)
            is_excluded_word = surface in excluded_words
            is_too_short = len(surface) <= 1

            if not is_excluded_pos and not is_excluded_word and not is_too_short:
                words.append(surface)

        return words

    def calculate_word_overlap(self, text1, text2):
        words1 = self.tokenize_japanese(text1)
        words2 = self.tokenize_japanese(text2)

        counter1 = Counter(words1)
        counter2 = Counter(words2)

        common = counter1 & counter2
        total = counter2

        overlap = sum(common.values())
        total_count = sum(total.values())

        return (overlap / total_count) if total_count > 0 else 0, words1, words2, common

    def calculate_vector_similarity(self, text1, text2):
        vec1 = self.embeddings.encode_single(text1)
        vec2 = self.embeddings.encode_single(text2)

        vec1 = np.array(vec1)
        vec2 = np.array(vec2)

        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        if norm1 == 0 or norm2 == 0:
            return 0

        return dot_product / (norm1 * norm2)

    def score_translation(self, user_translation, current_question=None, debug=False):
        scoring_details = {
            'steps': [],
            'normalized_user': '',
            'normalized_reference': '',
            'raw_similarity': 0.0
        }

        if not user_translation.strip():
            return {
                'score': 0,
                'feedback': '回答が入力されていません。',
                'grade': 'F',
                'reference_translation': None,
                'scoring_details': scoring_details
            }

        reference_translation = None
        best_score = 0

        scoring_details['steps'].append('📝 ステップ1: 正解の和訳を取得')

        if current_question and 'japanese' in current_question:
            reference_translation = current_question['japanese']
            scoring_details['steps'].append(f'✅ 正解: {reference_translation}')

            scoring_details['steps'].append('\n🔤 ステップ2: 形態素解析（単語分割・助詞除外）')

            word_overlap, user_words, ref_words, common_words = self.calculate_word_overlap(
                user_translation, reference_translation
            )

            scoring_details['user_words'] = user_words
            scoring_details['ref_words'] = ref_words
            scoring_details['common_words'] = list(common_words.elements())
            scoring_details['word_overlap'] = word_overlap

            scoring_details['steps'].append('※ 助詞（は、が、を、に等）は除外して評価')
            scoring_details['steps'].append(f'あなたの内容語数: {len(user_words)}個')
            scoring_details['steps'].append(f'正解の内容語数: {len(ref_words)}個')
            scoring_details['steps'].append(f'一致した単語数: {len(scoring_details["common_words"])}個')
            scoring_details['steps'].append(f'単語一致率: {word_overlap:.4f} ({word_overlap*100:.2f}%)')

            if scoring_details['common_words']:
                words_preview = '、'.join(scoring_details['common_words'][:15])
                if len(scoring_details['common_words']) > 15:
                    words_preview += f'... (他{len(scoring_details["common_words"])-15}個)'
                scoring_details['steps'].append(f'一致した単語: {words_preview}')

            scoring_details['steps'].append('\n🧮 ステップ3: ベクトル類似度計算（RAG方式）')

            vector_sim = self.calculate_vector_similarity(user_translation, reference_translation)
            scoring_details['vector_similarity'] = vector_sim

            scoring_details['steps'].append(f'ベクトル類似度（コサイン類似度）: {vector_sim:.4f} ({vector_sim*100:.2f}%)')
            scoring_details['steps'].append('※ 文章全体の意味的な近さを測定')

            scoring_details['steps'].append('\n📊 ステップ4: 文字列類似度計算')

            user_normalized = re.sub(r'[、。！？\s]+', '', user_translation.lower().strip())
            ref_normalized = re.sub(r'[、。！？\s]+', '', reference_translation.lower().strip())

            scoring_details['normalized_user'] = user_normalized
            scoring_details['normalized_reference'] = ref_normalized

            matcher = SequenceMatcher(None, user_normalized, ref_normalized)
            string_sim = matcher.ratio()
            scoring_details['string_similarity'] = string_sim

            total_len = len(ref_normalized)
            matched_len = 0
            common_parts = []
            diff_parts = []

            for tag, i1, i2, j1, j2 in matcher.get_opcodes():
                if tag == 'equal':
                    part = user_normalized[i1:i2]
                    common_parts.append(part)
                    matched_len += len(part)
                    diff_parts.append(('match', part, part))
                elif tag == 'replace':
                    diff_parts.append(('replace', user_normalized[i1:i2], ref_normalized[j1:j2]))
                elif tag == 'delete':
                    diff_parts.append(('delete', user_normalized[i1:i2], ''))
                elif tag == 'insert':
                    diff_parts.append(('insert', '', ref_normalized[j1:j2]))

            scoring_details['diff_parts'] = diff_parts
            scoring_details['matched_length'] = matched_len
            scoring_details['total_length'] = total_len

            scoring_details['steps'].append(f'文字列類似度: {string_sim:.4f} ({string_sim*100:.2f}%)')

            scoring_details['steps'].append('\n🎯 ステップ5: 総合スコア計算')

            weight_vector = 0.40
            weight_word = 0.40
            weight_string = 0.20

            best_score = (
                vector_sim * weight_vector +
                word_overlap * weight_word +
                string_sim * weight_string
            )

            scoring_details['raw_similarity'] = best_score
            scoring_details['weights'] = {
                'vector': weight_vector,
                'word': weight_word,
                'string': weight_string
            }

            scoring_details['steps'].append(f'計算式: (ベクトル類似度 × {weight_vector}) + (単語一致率 × {weight_word}) + (文字列類似度 × {weight_string})')
            scoring_details['steps'].append(f'= ({vector_sim:.3f} × {weight_vector}) + ({word_overlap:.3f} × {weight_word}) + ({string_sim:.3f} × {weight_string})')
            scoring_details['steps'].append(f'= {vector_sim*weight_vector:.3f} + {word_overlap*weight_word:.3f} + {string_sim*weight_string:.3f}')
            scoring_details['steps'].append(f'= {best_score:.4f}')

        else:
            scoring_details['steps'].append('⚠️ 正解データが見つかりません（検索中...）')
            english_text = current_question.get('english', '') if current_question else ''
            all_docs = self.vector_store.get_all_documents()

            for doc in all_docs:
                doc_text = doc['text']

                if 'EN:' in doc_text and 'JP:' in doc_text:
                    lines = doc_text.split('\n')
                    english_line = None
                    japanese_line = None

                    for line in lines:
                        if line.startswith('EN:'):
                            english_line = line.replace('EN:', '').strip()
                        elif line.startswith('JP:'):
                            japanese_line = line.replace('JP:', '').strip()

                    if english_line and japanese_line:
                        en_normalized = english_line.strip().lower()
                        query_normalized = english_text.strip().lower()

                        if en_normalized == query_normalized:
                            similarity = self.calculate_similarity(user_translation, japanese_line)

                            if similarity > best_score:
                                best_score = similarity
                                reference_translation = japanese_line

        score = int(best_score * 100)
        scoring_details['steps'].append(f'\n🎯 最終スコア: {score}点')

        if score >= 90:
            grade = 'S'
            feedback = '素晴らしい！ほぼ完璧な翻訳です。'
        elif score >= 80:
            grade = 'A'
            feedback = '非常に良い翻訳です！'
        elif score >= 70:
            grade = 'B'
            feedback = '良い翻訳です。いくつか改善点があります。'
        elif score >= 60:
            grade = 'C'
            feedback = 'まずまずです。もう少し正確に翻訳しましょう。'
        elif score >= 40:
            grade = 'D'
            feedback = '意味は伝わっていますが、改善が必要です。'
        else:
            grade = 'F'
            feedback = '翻訳の精度が低いです。再度チャレンジしましょう。'

        result = {
            'score': score,
            'grade': grade,
            'feedback': feedback,
            'english': current_question.get('english', '') if current_question else '',
            'reference_translation': reference_translation,
            'scoring_details': scoring_details
        }

        self.score_history.append(result)

        return result

    def extract_japanese_sentences(self, text):
        sentences = re.split(r'[。！？\n]', text)

        japanese_sentences = []
        for sentence in sentences:
            sentence = sentence.strip()

            if len(sentence) < 10:
                continue

            japanese_chars = sum(1 for c in sentence if '\u3040' <= c <= '\u309F' or '\u30A0' <= c <= '\u30FF' or '\u4E00' <= c <= '\u9FFF')

            if japanese_chars / len(sentence) > 0.3:
                japanese_sentences.append(sentence)

        return japanese_sentences

    def get_statistics(self):
        if not self.score_history:
            return None

        scores = [result['score'] for result in self.score_history]

        return {
            'total_questions': len(self.score_history),
            'average_score': sum(scores) / len(scores),
            'highest_score': max(scores),
            'lowest_score': min(scores),
            'grade_distribution': self._calculate_grade_distribution()
        }

    def _calculate_grade_distribution(self):
        grades = {}
        for result in self.score_history:
            grade = result['grade']
            grades[grade] = grades.get(grade, 0) + 1
        return grades


def main():
    print("=" * 60)
    print("🎓 English Quiz System - RAGベースの英語学習システム")
    print("=" * 60)

    quiz = EnglishQuizSystem()

    print(f"\n📚 利用可能なドキュメント数: {len(quiz.vector_store.documents)}")

    if len(quiz.vector_store.documents) == 0:
        print("\n⚠️ ドキュメントがありません。")
        print("先にPDFファイルをRAGシステムに追加してください。")
        return

    while True:
        print("\n" + "=" * 60)
        question = quiz.get_random_english_question()

        if not question:
            print("❌ 英文が見つかりませんでした。")
            break

        print("\n📖 以下の英文を和訳してください:")
        print("-" * 60)
        print(question['english'])
        print("-" * 60)
        print(f"出典: {os.path.basename(question['source'])}")

        user_translation = input("\n✏️ あなたの和訳を入力してください: ").strip()

        if user_translation.lower() in ['quit', 'exit', 'q']:
            print("\n👋 終了します。")
            break

        print("\n⏳ 採点中...")
        result = quiz.score_translation(user_translation, question['english'])

        print("\n" + "=" * 60)
        print("📊 採点結果")
        print("=" * 60)
        print(f"スコア: {result['score']}点")
        print(f"グレード: {result['grade']}")
        print(f"フィードバック: {result['feedback']}")
        print("=" * 60)

        continue_choice = input("\n次の問題に進みますか？ (y/n): ").strip().lower()

        if continue_choice != 'y':
            break

    stats = quiz.get_statistics()
    if stats:
        print("\n" + "=" * 60)
        print("📈 学習統計")
        print("=" * 60)
        print(f"総問題数: {stats['total_questions']}")
        print(f"平均スコア: {stats['average_score']:.1f}点")
        print(f"最高スコア: {stats['highest_score']}点")
        print(f"最低スコア: {stats['lowest_score']}点")
        print(f"\nグレード分布:")
        for grade, count in sorted(stats['grade_distribution'].items()):
            print(f"  {grade}: {count}回")
        print("=" * 60)


if __name__ == "__main__":
    main()
