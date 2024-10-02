import streamlit as st

from word_search import process_word_search


def main():

    st.markdown("""
        <style>
        .stTextInput>div>div>input {
            font-family: 'Verdana', sans-serif;  
            color: #000000; 
            width: 400px;  
            height: 50px;  
            padding: 10px;  
            border-radius: 5px;  
        }
        .stButton>button {
            font-family: 'Courier New', Courier, monospace;  
        }
        .text-background {
            background-color: rgba(255, 255, 255, 0.8);  
            padding:20px; 
            border-radius: 10px;  
            box-shadow: 0px 40px 10px rgba(0, 0, 0, 0.2);  
            width: 500px;  
            height: 200px;
        }
        </style>
        """, unsafe_allow_html=True)

    st.title("word search!")

    word = st.text_input("Enter a word:")
    search_button = st.button("search")

    if search_button and word:
        #with st.spinner('Searching...'):
        result = process_word_search.main(word)
            
        if "error" in result:
            st.error(result["error"])
        else:
            st.write(f"Word: {result['word']}")
            st.write(f"Meaning: {result['meaning']}")
            st.write(f"Search Count: {result['search_count']}")
            st.write(f"Example Sentence: {result['example_sentence']}")

main()

if __name__ == '__main__':
    main()