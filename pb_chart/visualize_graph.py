import streamlit as st
import math
import random
import numpy as np
import pandas as pd
from streamlit.components.v1 import html

from pb_chart.move_bubbles import move_bubbles_towards_center, place_bubbles_on_circle
# move bubbles_toward_center: 適当な位置の円の集合を設定した中心に円同士が重ならないように近づける関数
# place_bubbles_on_circle: 最初の初期位置を適当ではなく，円周上に均等に配置する関数
from pb_chart.bubble_UI import write_UI
# cssとjavascript,htmlを書かせるプログラムを隔離した
 


df = pd.read_csv('database/word_db.csv')
df.loc[df['Search Count'] > 6, 'Search Count'] = 50
df.loc[(df['Search Count'] <= 6) & (df['Search Count'] >=3), 'Search Count'] = 35
df.loc[df['Search Count'] < 3, 'Search Count'] = 20
df = df.sort_values('Search Count', ascending=False)
# バブルを配置するパラメータ
num_bubbles = [len(df[df['Search Count'] == 50]), len(df[df['Search Count'] == 35]), len(df[df['Search Count'] == 20])]  # バブルの数
center_x, center_y = 300, 300  # 円の中心
radius = [60, 40, 20]  # 円の半径

# バブルの初期位置を円周上に均等に配置
x_positions, y_positions = place_bubbles_on_circle(num_bubbles[0], center_x, center_y, radius[0])
x_positions2, y_positions2 = place_bubbles_on_circle(num_bubbles[1], center_x, center_y, radius[1]*10)
x_positions3, y_positions3 = place_bubbles_on_circle(num_bubbles[2], center_x, center_y, radius[2]*25)

x_positions.extend(x_positions2)
x_positions.extend(x_positions3)

y_positions.extend(y_positions2)
y_positions.extend(y_positions3)

df['x'] = x_positions
df['y'] = y_positions
# バブルの半径（例: 固定または可変）
df = df.sample(n=50)
radii =  df['Search Count'].values.tolist() # [40, 50, 60, 55, 25, 34, 60, 30]
name = df['Word'].values.tolist()
mean = df['Meaning'].values.tolist()
example = df['Example Sentence'].values.tolist()
x = df['x'].values.tolist()
y = df['y'].values.tolist()
num_bubbles = len(radii)
# バブルを中心に寄せる
x, y = move_bubbles_towards_center(num_bubbles, x, y, center_x, center_y, radii, speed=1, iterations=250)
# CSSとHTMLでボタンを配置

# HTMLをStreamlitで表示
button_html = write_UI(num_bubbles, radii, x, y, name, mean, example)
html(button_html, width=1000, height=1000)