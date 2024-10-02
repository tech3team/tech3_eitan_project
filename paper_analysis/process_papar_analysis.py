import spacy
import re
from collections import Counter
from unstructured.partition.pdf import partition_pdf
from deep_translator import GoogleTranslator

# SpaCyのモデルをロード（英語モデル）
nlp = spacy.load('en_core_web_sm')

# PDFからテキストを抽出する関数
def extract_text_from_pdf(uploaded_file):
    elements = partition_pdf(file=uploaded_file)
    
    # テキストを結合
    text = ''.join([str(element) for element in elements])
    
    # ハイフンで分割された単語を結合
    text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', text)
    
    # 改行をスペースに置き換え
    text = text.replace('\n', ' ')
    
    # 「References」以降のテキストを削除
    if 'References' in text:
        text = text.split('References')[0]
        
    return text

# 単語を翻訳する関数
def translate_word_list(words):
    translator = GoogleTranslator(source='en', target='ja')
    translated_words = {word: translator.translate(word) for word in words}
    return translated_words

# 単語フィルタリング関数
def filter_words(doc, selected_pos_tags):
    filtered_words = []
    for token in doc:
        if (token.pos_ in ['NOUN'] and '名詞' in selected_pos_tags) or \
           (token.pos_ in ['VERB'] and '動詞' in selected_pos_tags) or \
           (token.pos_ in ['ADJ'] and '形容詞' in selected_pos_tags) or \
           (token.pos_ in ['ADV'] and '副詞' in selected_pos_tags):
            filtered_words.append(token.text)
    return filtered_words

# 複合語の解析関数
def classify_compound_terms(doc, pos_options):
    compounds = {'形容詞修飾': [], '複合名詞': [], '分詞': [], '副詞修飾': []}
    for token in doc:
        if token.pos_ == 'ADJ' and token.dep_ == 'amod' and '形容詞修飾' in pos_options:
            compounds['形容詞修飾'].append(f"{token.text} {token.head.text}")
        elif token.pos_ == 'NOUN' and token.dep_ == 'compound' and '複合名詞' in pos_options:
            compounds['複合名詞'].append(f"{token.head.text} {token.text}")
        elif token.tag_ in ['VBG', 'VBN'] and token.head.pos_ == 'NOUN' and '分詞' in pos_options:
            compounds['分詞'].append(f"{token.text} {token.head.text}")
        elif token.pos_ == 'ADV' and token.dep_ == 'advmod' and '副詞修飾' in pos_options:
            compounds['副詞修飾'].append(f"{token.text} {token.head.text}")
    return compounds

# 特定の単語を削除する関数
def clean_words(filtered_words, unwanted_words, be_verbs):
    return [word for word in filtered_words if 
            not re.search(r'\d', word) and  # 数字を含む単語を削除
            re.match(r'^[a-zA-Z ]+$', word) and  # A-Z,a-z,スペース以外の文字を含む単語を削除
            len(word) < 33 and  # 長すぎる単語を削除
            not any(be_verb in word for be_verb in be_verbs) and  # be動詞を削除
            not any(unwanted_word in word for unwanted_word in unwanted_words)]  # 特定の単語を削除