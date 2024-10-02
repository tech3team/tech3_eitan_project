import time
import streamlit as st

def main():
    st.set_page_config(
        page_title="AI単", 
        page_icon=":v:"
    )

    if 'next_screen' not in st.session_state:
        # ホーム画面表示
        st.title("AI単")
        st.image("images/push.png", width=200)

        time.sleep(3)
        st.session_state['next_screen'] = True
        st.rerun()

    word_search = st.Page(page="word_search/display_word_search.py", title="単語検索", icon=":material/home:", default=True)
    word_quiz = st.Page(page="word_quiz/display_word_quiz.py", title="単語テスト", icon=":material/quiz:")
    pb_chart = st.Page(page="pb_chart/visualize_graph.py", title="Voca鍋(仮)", icon=":material/apps:")
    paper_upload = st.Page(page="paper_analysis/display_paper_analysis.py", title="論文登録", icon=":material/description:")
    my_data = st.Page(page="mysetting/learning_profile.py", title="学習データ", icon=":material/monitoring:")
    setting = st.Page(page="mysetting/setting.py", title="設定", icon=":material/settings:")
    
    # スピナーを表示しつつナビゲーションを実行
    with st.spinner('ページを読み込んでいます...'):
        pg = st.navigation([word_search, pb_chart, word_quiz, paper_upload, my_data, setting])
        pg.run()

if __name__ == '__main__':
    main()
