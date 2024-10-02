import os
import glob
import openai
from openai import OpenAI
import pandas as pd
import json

from utils import load_api_key

def _find_files_recursively(pattern, search_directory='.'):
    """再帰的に全サブディレクトリを含めて検索"""
    search_pattern = os.path.join(search_directory, '**', pattern)
    files = glob.glob(search_pattern, recursive=True)

    return files[0]


def _load_csv(file_name):
    """csvファイルのの読み込み"""
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
    

def _extraction_from_thesis(df, n_word_test):
    """論文データからテストの単語抽出"""
    try:
        # 出現頻度が閾値以上のカラムをランダムに選択
        threshold = df['Appearance_Count'].quantile(0.75)
        df_selcted = df.query(f'Appearance_Count > {threshold}')
        top_words = df_selcted[['Word', 'Meaning']].sample(n=n_word_test)

        return top_words

    except Exception as e:
        print(f"データ処理中にエラーが発生しました: {e}")


def _extraction_from_basic(df, n_word_test):
    """基本データからテストする単語抽出"""
    try:
        # "検索回数"カラムで値が大きい順にソート
        df_sorted = df.sort_values(by="Search Count", ascending=False)
        # 上位N件（例: 5件）の"単語"と"意味"を取得
        top_words = df_sorted[['Word', 'Meaning']].head(n_word_test)

        # print(top_words)
        return top_words

    except Exception as e:
        print(f"データ処理中にエラーが発生しました: {e}")


def process_csv(file_name, n_word_test, quiz_mode):
    """
    csvより、クイズを作成する対象の単語をリストアップする
    
    Args:
        file_path (str): 対象csv名 ---.csv
        n_word_teste (int): 問題数
        quiz_mode (str): "基本単語モード" or "論文モード"

    Returns:
        top_words (dict): 問題とするWord,Meaning
    """
    
    df = _load_csv(file_name)
    
    # 読み込みが成功した場合のみ処理を続ける
    if df is not None:
        # 選択肢したモード別に単語をピックアップする
        if quiz_mode == '基本単語帳もーど':
            top_words = _extraction_from_basic(df, n_word_test)

        elif quiz_mode == '論文もーど':
            top_words = _extraction_from_thesis(df, n_word_test)

        return top_words

    else:
        print("CSVファイルの読み込みに失敗したため、処理を中止します。")


def _prompt_quiz_type(quiz_type: str, row: dict) -> str:
        """出題タイプ別のpromptにする関数"""
        word = row['Word']
        meaning = row['Meaning']

        # JSONフォーマットでリクエストメッセージを構築
        request_data = {
            "question": "ここに問題文",
            "choice4": ["選択肢A", "選択肢B", "選択肢C", "選択肢D"],
            "correct_answer": "選択肢A"
        }

        if quiz_type == '4択単語問題：英→日':
            message = f"""
                次の英単語をもとに、日本語の意味を選択する４択の問題を作成してください。: {word}の意味は「{meaning}」です。
                以下JSON形式で生成してください。
                {json.dumps(request_data, ensure_ascii=False)}
                """
            
        elif quiz_type == '4択単語問題：日→英':
            message = f"""
                次の単語の日本語の意味をもとに、英単語を選択する４択の問題を作成してください。: {word}の意味は「{meaning}」です。
                以下JSON形式で生成してください。
                {json.dumps(request_data, ensure_ascii=False)}
                """
            
        elif quiz_type == '4択和訳問題：英→日':
            message = f"""
                次の英単語使った英語例文を作成し、その和訳問題を作成してください。形式は４択の問題です。: {word}の意味は「{meaning}」です。
                以下JSON形式で生成してください。
                {json.dumps(request_data, ensure_ascii=False)}
                """
        
        return message
        

def generate_quiz(top_words, quiz_type):
    """
    gptのapiを使用し、問題を作成する

    Args:
        top_words (pd.DataFrame): 問題とするWord,Meaning
        quiz_type (str): '4択単語問題：日→英' or '4択単語問題：英→日' or '4択和訳問題：英→日'

    Returns:
        quiz_list (dict): 生成した辞書型クイズデータ question, choice4, correct_answer
    """

    api_key = load_api_key()

    client = OpenAI(
        api_key=api_key
    )  

    # クイズデータを保存するリスト
    quiz_list = []

    for index, row in top_words.iterrows():
        # 出題タイプ別のpromptを作成する
        message = _prompt_quiz_type(quiz_type, row)
        print(message)
        
        try:
            # print("APIリクエスト前")
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # GPTのエンジン名を指定します
                messages=[
                    {"role": "user", "content": f"/japanese {message}"}  # ユーザーのメッセージ
                ],
                max_tokens=100,  # 生成するトークンの最大数
                n=1,  # 生成するレスポンスの数
                stop=None,  # 停止トークンの設定
                temperature=0.5,  # 生成時のランダム性の制御
                top_p=1,  # トークン選択時の確率閾値
            )

            # 生成されたコンテンツを取得
            quiz_data = response.choices[0].message.content
            print(quiz_data)

            try:
                quiz_data_json = json.loads(quiz_data)
                print(quiz_data_json)
                quiz_list.append(quiz_data_json)
                print(quiz_list)

            except json.JSONDecodeError as e:
                print(f"JSONデコードエラー: {e}")

        except openai.RateLimitError as e:
            # APIリクエストがレート制限を超えたときのエラー
            print(f"レート制限に達しました。時間を置いて再試行してください: {e}")
        except openai.APITimeoutError as e:
            # リクエストに無効なパラメータが含まれていた場合のエラー
            print(f"リクエストがタイムアウトしました。: {e}")
        except openai.AuthenticationError as e:
            # APIキーの認証が失敗した場合のエラー
            print(f"APIキーの認証に失敗しました。キーを確認してください: {e}")
        except openai.APIConnectionError as e:
            # サーバーへの接続に問題があった場合のエラー
            print(f"APIサーバーへの接続に失敗しました。ネットワーク接続を確認してください: {e}")
        except openai.OpenAIError as e:
            # その他のOpenAI APIに関連するエラー
            print(f"OpenAI APIでエラーが発生しました: {e}")
        except Exception as e:
            # その他の汎用的なエラー
            print(f"不明なエラーが発生しました: {type(e).__name__}, {str(e)}")

    return quiz_list


if __name__ == '__main__':
    top_words = process_csv(file_name='word_list_spacy_top100.csv', n_word_test=2, quiz_mode="論文もーど")
    print(top_words)
