"""
Streamlit English Quiz Application
RAGシステムを使った英語学習アプリ（GUI版）
"""
import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from english_quiz_system import EnglishQuizSystem

st.set_page_config(
    page_title="English Quiz System",
    page_icon="🎓",
    layout="wide"
)

if 'quiz_system' not in st.session_state:
    st.session_state.quiz_system = EnglishQuizSystem()
    st.session_state.current_question = None
    st.session_state.user_answer = ""
    st.session_state.result = None
    st.session_state.show_result = False
    st.session_state.setup_complete = False

quiz = st.session_state.quiz_system

if not st.session_state.setup_complete and len(quiz.vector_store.documents) == 0:
    with st.spinner('初回セットアップ中...サンプルデータを作成しています...'):
        try:
            from create_sample_data import create_sample_data
            create_sample_data()
            st.session_state.setup_complete = True
            st.rerun()
        except Exception as e:
            st.error(f"セットアップエラー: {e}")
            st.stop()

st.title("🎓 English Quiz System")
st.markdown("RAGシステムから英文を抽出し、和訳を採点します")

st.sidebar.header("📊 システム情報")
doc_count = len(quiz.vector_store.documents)
st.sidebar.metric("📚 利用可能なドキュメント数", doc_count)

if doc_count == 0:
    st.error("⚠️ データの読み込みに失敗しました。ページをリロードしてください。")
    st.stop()

stats = quiz.get_statistics()
if stats:
    st.sidebar.divider()
    st.sidebar.header("📈 学習統計")
    st.sidebar.metric("📝 総問題数", stats['total_questions'])
    st.sidebar.metric("⭐ 平均スコア", f"{stats['average_score']:.1f}点")
    st.sidebar.metric("🏆 最高スコア", f"{stats['highest_score']}点")

    if stats['grade_distribution']:
        st.sidebar.write("**グレード分布:**")
        for grade in ['S', 'A', 'B', 'C', 'D', 'F']:
            count = stats['grade_distribution'].get(grade, 0)
            if count > 0:
                st.sidebar.write(f"{grade}: {count}回")

st.sidebar.divider()
if st.sidebar.button("🔄 統計をリセット"):
    st.session_state.quiz_system.score_history = []
    st.rerun()

col1, col2 = st.columns([2, 1])

with col1:
    st.header("📖 問題")

    if st.session_state.current_question is None or st.button("🎲 新しい問題を出題", type="primary"):
        st.session_state.current_question = quiz.get_random_english_question()
        st.session_state.user_answer = ""
        st.session_state.result = None
        st.session_state.show_result = False

        if st.session_state.current_question:
            st.rerun()

    if st.session_state.current_question:
        question = st.session_state.current_question

        st.subheader("以下の英文を和訳してください:")

        st.info(question['english'])

        st.caption(f"📄 出典: {os.path.basename(question['source'])}")

        st.divider()

        user_answer = st.text_area(
            "✏️ あなたの和訳を入力してください:",
            value=st.session_state.user_answer,
            height=150,
            key="answer_input"
        )

        st.session_state.user_answer = user_answer

        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:
            if st.button("📝 採点する", type="primary", disabled=not user_answer.strip()):
                st.session_state.result = quiz.score_translation(
                    user_answer,
                    current_question=question
                )
                st.session_state.show_result = True
                st.rerun()

        with col_btn2:
            if st.button("⏭️ スキップ"):
                st.session_state.current_question = quiz.get_random_english_question()
                st.session_state.user_answer = ""
                st.session_state.result = None
                st.session_state.show_result = False
                st.rerun()

with col2:
    st.header("💡 ヒント")

    if st.session_state.current_question:
        st.write("**翻訳のポイント:**")
        st.write("- 文章全体の意味を理解する")
        st.write("- 自然な日本語に翻訳する")
        st.write("- 主語・述語を明確にする")

        sentence = st.session_state.current_question['english']
        word_count = len(sentence.split())
        char_count = len(sentence)

        st.divider()
        st.metric("📏 単語数", word_count)
        st.metric("📏 文字数", char_count)

if st.session_state.show_result and st.session_state.result:
    st.divider()

    result = st.session_state.result

    st.header("📊 採点結果")

    col_result1, col_result2, col_result3 = st.columns(3)

    with col_result1:
        st.metric("スコア", f"{result['score']}点")

    with col_result2:
        grade_colors = {
            'S': '🌟',
            'A': '✨',
            'B': '⭐',
            'C': '💫',
            'D': '🔆',
            'F': '💧'
        }
        grade_icon = grade_colors.get(result['grade'], '')
        st.metric("グレード", f"{grade_icon} {result['grade']}")

    with col_result3:
        st.metric("総問題数", len(quiz.score_history))

    if result['score'] >= 80:
        st.success(result['feedback'])
    elif result['score'] >= 60:
        st.info(result['feedback'])
    else:
        st.warning(result['feedback'])

    st.write("**出題された英文:**")
    st.code(result['english'], language="text")

    st.write("**あなたの回答:**")
    st.code(st.session_state.user_answer, language="text")

    if result.get('reference_translation'):
        st.write("**参考訳:**")
        st.info(result['reference_translation'])

    if result.get('scoring_details'):
        st.divider()
        with st.expander("🔍 採点の詳細を見る", expanded=False):
            details = result['scoring_details']

            st.markdown("### 採点プロセス")

            for step in details['steps']:
                st.write(step)

            if details.get('normalized_user') and details.get('normalized_reference'):
                st.divider()
                st.markdown("### 📊 類似度計算の詳細")

                st.subheader("📈 各指標のスコア")

                col_score1, col_score2, col_score3 = st.columns(3)

                with col_score1:
                    if details.get('vector_similarity') is not None:
                        st.metric("🧮 ベクトル類似度",
                                f"{details['vector_similarity']*100:.1f}%",
                                help="RAG方式の意味的類似度")

                with col_score2:
                    if details.get('word_overlap') is not None:
                        st.metric("🔤 単語一致率",
                                f"{details['word_overlap']*100:.1f}%",
                                help="内容語（助詞除外）の一致度")

                with col_score3:
                    if details.get('string_similarity') is not None:
                        st.metric("📊 文字列類似度",
                                f"{details['string_similarity']*100:.1f}%",
                                help="文字レベルの一致度")

                if details.get('weights'):
                    st.info(f"⚖️ **重み配分:** ベクトル{details['weights']['vector']*100:.0f}% + 単語{details['weights']['word']*100:.0f}% + 文字列{details['weights']['string']*100:.0f}%")

                if details.get('raw_similarity'):
                    st.progress(details['raw_similarity'], text=f"最終類似度スコア: {details['raw_similarity']*100:.2f}%")

                st.divider()
                st.markdown("### 🔤 単語レベルの分析（助詞除外）")
                st.caption("※ 「は」「が」「を」「に」などの助詞は除外して評価しています")

                if details.get('user_words') and details.get('ref_words'):
                    col_word1, col_word2 = st.columns(2)

                    with col_word1:
                        st.write("**あなたの内容語:**")
                        user_words_display = ' | '.join(details['user_words'][:20])
                        if len(details['user_words']) > 20:
                            user_words_display += f' | ... (+{len(details["user_words"])-20})'
                        st.code(user_words_display, language="text")

                    with col_word2:
                        st.write("**正解の内容語:**")
                        ref_words_display = ' | '.join(details['ref_words'][:20])
                        if len(details['ref_words']) > 20:
                            ref_words_display += f' | ... (+{len(details["ref_words"])-20})'
                        st.code(ref_words_display, language="text")

                    if details.get('common_words'):
                        st.success(f"✅ 一致した単語（{len(details['common_words'])}個）: {', '.join(details['common_words'][:20])}")
                        if len(details['common_words']) > 20:
                            st.caption(f"... 他{len(details['common_words'])-20}個")

                st.divider()
                st.markdown("### 🔍 文字列比較（正規化後）")

                if details.get('diff_parts'):
                    st.write("**差分表示:**")

                    user_html = ""
                    ref_html = ""

                    for tag, user_part, ref_part in details['diff_parts']:
                        if tag == 'match':
                            user_html += f'<span style="background-color: #90EE90; color: black;">{user_part}</span>'
                            ref_html += f'<span style="background-color: #90EE90; color: black;">{ref_part}</span>'
                        elif tag == 'replace':
                            user_html += f'<span style="background-color: #FFB6C1; color: black; text-decoration: line-through;">{user_part}</span>'
                            ref_html += f'<span style="background-color: #87CEEB; color: black;">{ref_part}</span>'
                        elif tag == 'delete':
                            user_html += f'<span style="background-color: #FFB6C1; color: black; text-decoration: line-through;">{user_part}</span>'
                        elif tag == 'insert':
                            ref_html += f'<span style="background-color: #87CEEB; color: black;">{ref_part}</span>'

                    col_diff1, col_diff2 = st.columns(2)
                    with col_diff1:
                        st.markdown("**あなたの回答:**")
                        st.markdown(f'<div style="padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-family: monospace; line-height: 1.8;">{user_html}</div>', unsafe_allow_html=True)
                    with col_diff2:
                        st.markdown("**正解:**")
                        st.markdown(f'<div style="padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-family: monospace; line-height: 1.8;">{ref_html}</div>', unsafe_allow_html=True)

                    st.markdown("""
                    **凡例:**
                    - <span style="background-color: #90EE90; padding: 2px 5px;">緑</span> = 一致
                    - <span style="background-color: #FFB6C1; padding: 2px 5px;">ピンク（取り消し線）</span> = あなたが書いた部分（不要/誤り）
                    - <span style="background-color: #87CEEB; padding: 2px 5px;">青</span> = 正解にある部分（不足）
                    """, unsafe_allow_html=True)

                else:
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.write("**あなたの回答（正規化）**")
                        st.code(details['normalized_user'], language="text")
                    with col_b:
                        st.write("**正解（正規化）**")
                        st.code(details['normalized_reference'], language="text")

                st.divider()
                st.info("💡 **採点方法:** 句読点とスペースを除去した後、文字列の類似度を計算しています。SequenceMatcher（Python標準ライブラリ）を使用して、一致する部分と異なる部分を検出し、全体の類似度を0-1のスコアで算出します。")

st.divider()

with st.expander("📚 学習履歴"):
    if quiz.score_history:
        st.write(f"**全{len(quiz.score_history)}問の結果:**")

        for i, record in enumerate(reversed(quiz.score_history[-10:]), 1):
            col_hist1, col_hist2, col_hist3 = st.columns([3, 1, 1])

            with col_hist1:
                preview = record['english'][:60] + "..." if len(record['english']) > 60 else record['english']
                st.write(f"{i}. {preview}")

            with col_hist2:
                st.write(f"グレード: {record['grade']}")

            with col_hist3:
                st.write(f"{record['score']}点")

        if len(quiz.score_history) > 10:
            st.caption(f"... 他 {len(quiz.score_history) - 10}問")
    else:
        st.info("まだ問題に挑戦していません。")

st.markdown("---")
st.markdown("🎓 **English Quiz System** - RAGシステムを活用した英語学習ツール")