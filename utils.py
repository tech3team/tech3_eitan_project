import streamlit as st
import os
import pandas as pd
import json

try:
    import cv2
except ImportError:
    from PIL import Image
    cv2 = Image  # cv2 の代わりに Pillow を使用する

def load_csv(file_name):
    """csvファイルの読み込み"""
    file_path = os.path.join('database', file_name)
    print(file_path)

    try:
        df = pd.read_csv(file_path)
        return df
    
    except FileNotFoundError:
        print(f"エラー: ファイル '{file_path}' が見つかりません。パスを確認してください。")
        return None
    except Exception as e:
        print(f"エラー: {e}")
        return None

def load_api_key():
    """api_keyの取得"""
    with open('config.json', 'r') as file:
        config = json.load(file)

    api_key = config.get('api_key')

    return api_key

def display_image(image_path):
    """画像を表示する関数"""
    try:
        img = cv2.imread(image_path)  # cv2 を使用して画像を読み込む
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # BGR から RGB に色空間を変換
        st.image(img, caption=image_path, use_column_width=True)
    except Exception as e:
        st.error(f"画像の表示中にエラーが発生しました: {e}")
