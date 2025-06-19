import os
import pandas as pd
import streamlit as st

from word_search.process_word_search_EJ import main as main_EJ
from word_search.process_word_search_JE import main as main_JE
from utils import load_csv
# from word_search.audio import main as audio_main  # word_search.audio を使用


def main():
    csv_file = "word_db.csv"
    df = load_csv(csv_file)

    st.title("単語検索")

    # 👇 key をつけた radio（1回のみ呼び出すように注意）
    mode = st.radio("モードを選択してください:", ('和英もーど', '英和もーど'), horizontal=True, key="mode_radio_1")
    word = st.text_input("単語入力:", key="word_input")
    category = st.selectbox(
        '分野選択:',
        ['認知科学', '強化学習', 'データ分析', 'その他'],
        index=None,
        placeholder="登録する分野を選択してください",
        key="category_select"
    )
    search_button = st.button("検索", key="search_button")

    if search_button and word:
        if mode == '和英もーど':
            result = main_JE(word, category, df)
        else:
            result = main_EJ(word, category, df)

        # audio_main(word)  # オーディオ呼び出しが必要ならここで有効に

        if "error" in result:
            st.error(result["error"])
        else:
            st.info(f"Word:　{result['word']}")
            st.info(f"Meaning:　{result['meaning']}")
            st.info(f"Pronounce:　{result['pronounce']}")
            st.info(f"Example Sentence:　{result['example_sentence']}")
            st.info(f"Translated Sentence:　{result['translated_sentence']}")
            st.info(f"Search Count:　{result['search_count']}")
            st.info(f"Category:　{category}")


# ✅ Streamlitではこれだけで十分
if __name__ == '__main__':
    main()
