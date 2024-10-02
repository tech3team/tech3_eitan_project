import streamlit as st
import pandas as pd
from collections import Counter
from paper_analysis.process_papar_analysis import extract_text_from_pdf, translate_word_list, filter_words, classify_compound_terms, clean_words

# SpaCyのモデルをロード（英語モデル）
import spacy
nlp = spacy.load('en_core_web_sm')

# タイトル
st.title("英語論文から英単語を抽出するアプリ")

# サイドバーは非使用
st.write("抽出したい品詞と複合語のオプションを選択してください:")
pos_options = st.multiselect(
    "抽出する品詞を選択してください",
    options=['名詞', '動詞', '形容詞', '副詞', '形容詞修飾', '複合名詞', '分詞', '副詞修飾'],
    default=['名詞', '動詞', '形容詞', '副詞']
)

# 表示する単語数のスライダー
word_count_slider = st.slider("表示する単語数を選択してください", min_value=10, max_value=200, value=100, step=10)

# PDFファイルのアップロード
uploaded_file = st.file_uploader("PDFファイルをアップロードしてください", type="pdf")

# 解析ボタン
if st.button("解析開始"):
    if uploaded_file is not None:
        # PDFのテキストを抽出する
        text = extract_text_from_pdf(uploaded_file)

        if text:
            st.write("テキストの抽出が完了しました！")

            # テキストをトークン化（品詞分解）
            doc = nlp(text.lower())

            # 単語のフィルタリング
            filtered_words = filter_words(doc, pos_options)

            # 複合語の解析を行う（必要に応じて）
            classified_terms = classify_compound_terms(doc, pos_options)
            for category, terms in classified_terms.items():
                for term in terms:
                    filtered_words.append(term)

            # be動詞と不要な単語を削除
            be_verbs = ['is', 'are', 'am', 'was', 'were', 'be', 'being', 'been']
            unwanted_words = ['as', 'much', 'also', 'such']
            cleaned_words = clean_words(filtered_words, unwanted_words, be_verbs)

            # 単語の出現頻度をカウント
            word_freq = Counter(cleaned_words)
            most_common_words = word_freq.most_common(word_count_slider)

            # 翻訳
            st.write("単語を翻訳中...")
            word_list = [word for word, freq in most_common_words]
            translated_words = translate_word_list(word_list)

            # 結果をデータフレームにまとめる
            df = pd.DataFrame(most_common_words, columns=['Word', 'Appearance Frequency'])
            df['Meaning'] = df['Word'].map(translated_words)
            df['Search Count'] = ''  # 空の列を追加
            df['Example Sentence'] = ''  # 空の列を追加

            # データフレームを表示
            st.write(df)

            # CSVダウンロード機能
            csv = df.to_csv(index=False)
            st.download_button("CSVファイルとしてダウンロード", csv, file_name="word_list.csv", mime="text/csv")
        else:
            st.write("PDFからテキストを抽出できませんでした。")
    else:
        st.write("PDFファイルをアップロードしてください。")