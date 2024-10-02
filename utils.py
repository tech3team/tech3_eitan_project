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
    "" ローカル環境で動かす場合には、以下を実行する ""
    #with open('config.json', 'r') as file:
    #    config = json.load(file)
    #api_key = config.get('api_key')

    "" Streamlit Cloud上で動かす場合には、以下を実行する 
    api_key = st.secrets[APIkeys][OPENAI_API_KEY]

    return api_key
