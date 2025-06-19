import streamlit as st
import pandas as pd
from streamlit.components.v1 import html

from pb_chart.move_bubbles import move_bubbles_towards_center, prepare_word_bubbles, prepare_paper_bubbles
from pb_chart.bubble_UI import write_UI_visualize, write_UI_burst, write_paper_UI_visualize

center_x, center_y = 200, 300  # 円の中心

# セッションの状態を初期化
if 'selected_options' not in st.session_state:
    st.session_state.selected_options = []

if 'delete_pressed' not in st.session_state:
    st.session_state['delete_pressed'] = False

# データを読み込み
# word_df = pd.read_csv('database/word_db.csv')
# paper_df = pd.read_csv('../test_python/paper_db.csv')


# タブの設定
tabs = st.tabs(['英単語', 'おはじけ'])

# 1つ目のタブ（英単語タブ）
with tabs[0]:
    st.write("英単語の可視化を選択しました。")
    # データを読み込み
    word_df = pd.read_csv('database/word_db.csv')

    radii, name, mean, example, color, x, y, num_bubbles, count = prepare_word_bubbles(word_df, 0)
    x, y = move_bubbles_towards_center(num_bubbles, x, y, center_x, center_y, radii, speed=1.5, iterations=400)

    # st.multiselectが表示されたまま、HTMLコンポーネントも表示
    # st.write("選択された単語:", selected_options)
    html(write_UI_visualize(num_bubbles, radii, x, y, name, mean, example, color, count), width=1000, height=1000)


# 2つ目のタブ（論文タブ）
# with tabs[1]:
#     st.write("論文の可視化を選択しました。")
#     # データを読み込み
#     paper_df = pd.read_csv('database/paper_db.csv')

#     radii, name, mean, color, x, y, num_bubbles, count = mendo_paper(paper_df, 0)
#     x, y = move_bubbles_towards_center(num_bubbles, x, y, center_x, center_y, radii, speed=1, iterations=300)

#     # HTMLコンポーネントを表示
#     html(write_paper_UI_visualize(num_bubbles, radii, x, y, name, mean, color, count), width=1000, height=1000)


# 3つ目のタブ（おはじけタブ）
with tabs[1]:
    st.write("おはじけの可視化を選択しました。")
    # データを読み込み
    word_df = pd.read_csv('database/word_db.csv')

    # 削除ボタンを追加
    if st.button('削除', key='delete'):
        st.session_state['delete_pressed'] = True

    # 削除ボタンが押された場合の処理
    if st.session_state['delete_pressed']:
        st.write("削除ボタンが押されました。処理を実行します。")

        # おはじけに関する処理
        radii, name, mean, example, color, x, y, num_bubbles, count = prepare_word_bubbles(word_df, 2)
        x, y = move_bubbles_towards_center(num_bubbles, x, y, center_x, center_y, radii, speed=1.5, iterations=300)

        # 削除アニメーションを実行するHTMLコンポーネント
        html(write_UI_burst(num_bubbles, radii, x, y, name, mean, example, color), width=1000, height=1000)

        # df.loc[df['Done']  ==  2, 'Done'] = 0
        # df.to_csv('../test_python/word_db.csv')

        # 状態をリセットすることで、次の削除ボタンを押すまでHTMLの動作を停止
        st.session_state['delete_pressed'] = False
