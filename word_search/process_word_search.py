import os
import pandas as pd
import openai
from openai import OpenAI
import json

from utils import load_api_key

csv_file = 'database/word_db.csv'

def search_word(word, df):
    api_key = load_api_key()

    client = OpenAI(
        api_key=api_key
    )
        
    if word in df['Word'].values:
        df.loc[df['Word'] == word, 'Search Count'] += 1
    else:
        new_row = pd.DataFrame({"Word": [word], "Meaning": [""], "Search Count": [1], "Example Sentence": [""]})
        df = pd.concat([df, new_row], ignore_index=True)
    
    request_data = {
                "meaning": "検索された単語の意味",
                "Example sentence": "検索された単語の例文"
    }
    
    message = f"""
                {word}の意味とその例文を教えてください。
                意味は日本語、例文は英語でお願いします。
                以下JSON形式で生成してください。
                {json.dumps(request_data, ensure_ascii=False)}
                """
    
    response = client.chat.completions.create(
                model="gpt-3.5-turbo",  #4o-minにする
                messages=[
                    {"role": "user", "content": f"/japanese {message}"}  
                ],
                max_tokens=50,  
                n=1, 
                stop=None,  
                temperature=0.5,  
                top_p=1,  
    )

    output = response.choices[0].message.content
    data_json = json.loads(output)
    # print(data_json)
    
    search_count = df.loc[df['Word'] == word, 'Search Count'].values[0]
    df.loc[df['Word'] == word, 'Meaning'] = data_json['meaning']
    df.loc[df['Word'] == word, 'Example Sentence'] = data_json['Example sentence']
    
    df.to_csv(csv_file, index=False)

    return {
            "word": word,
            "meaning": data_json['meaning'],
            "search_count": search_count,
            "example_sentence": data_json['Example sentence']
    }


def main(word):
    # CSVファイルが存在しない場合は新規作成
    if not os.path.exists(csv_file):
        df = pd.DataFrame(columns=["Word", "Meaning", "Search Count", "Example Sentence"])
        df.to_csv(csv_file, index=False)

    df = pd.read_csv(csv_file)

    return search_word(word, df)
