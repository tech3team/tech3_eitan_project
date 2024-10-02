import os
import sys
import streamlit as st
import pandas as pd

# sys.path.append("../")
from word_quiz.process_word_quiz import process_csv, generate_quiz


def display_quiz(quiz_list):
    """生成したクイズのリストから、順に取り出し表示する"""
    if 'current_quiz_index' not in st.session_state:
        st.session_state.current_quiz_index = 0
        st.session_state.score = 0
    
    # 今回のクイズを取得
    current_quiz = quiz_list[st.session_state.current_quiz_index]

    st.title("4択問題")
    st.write(f"**問題:** {current_quiz['question']}")

    # 選択肢の表示とユーザーの選択を取得
    user_choice = st.radio("選択肢:", current_quiz['choice4'])

    # 提出ボタン
    if st.button("回答"):
        if user_choice == current_quiz['correct_answer']:
            st.session_state.score += 1
            st.write("正解！")
        else:
            st.write(f"不正解！正しい答えは: {current_quiz['correct_answer']}")
            
        # 次のクイズに進む
        if st.session_state.current_quiz_index < len(quiz_list) - 1:
            st.session_state.current_quiz_index += 1
            st.rerun() # 画面を再描画して次のクイズを表示
        else:
            st.write(f"すべての問題が終了しました。正解数: {st.session_state.score}/{len(quiz_list)}")


def main():
    """クイズがスタートする画面表示"""
    
    if 'quiz_list' not in st.session_state:
        # 問題モードの選択
        quiz_mode = st.radio(
            "問題のタイプを選択してください:", 
            ('基本単語帳もーど', '論文もーど'), 
            horizontal=True)
        
        # 出題方法の選択
        quiz_type = st.selectbox(
            "出題の方法を指定してください:",
            ['4択単語問題：日→英', '4択単語問題：英→日', '4択和訳問題：英→日'],
            index = 1)
        
        # 出題方法からファイルパスを選ぶ
        if quiz_mode == "基本単語帳もーど":
            file_name="word_db.csv"
        elif quiz_mode == "論文もーど":
            file_name="word_list_spacy_top100.csv"
        
        # 問題数を指定する
        n_word_test = st.selectbox(
            "問題数を指定してください:",
            [2, 5, 10, 20, 50],
            index = 1)
        
        if st.button("この設定で開始する"):
            top_words = process_csv(file_name, n_word_test, quiz_mode) # CSVの処理
            print(top_words)
            quiz_list = generate_quiz(top_words, quiz_type)  # クイズの生成
            st.session_state.quiz_list = quiz_list  # セッション状態に保存
            st.rerun()
    
    # クイズが生成されていれば問題の表示
    elif 'quiz_list' in st.session_state:
        display_quiz(st.session_state.quiz_list)

main()

if __name__ == '__main__':
    main()