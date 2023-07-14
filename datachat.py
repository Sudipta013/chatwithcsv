import streamlit as st
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
from dotenv import load_dotenv
import os
import pandas as pd
from pandasai import PandasAI

OPENAI_API_KEY= st.secrets["auth_token"]

def chat_with_csv(df,prompt):
     llm = OpenAI(temperature=0,openai_api_key="OPENAI_API_KEY")
     pandas_ai = PandasAI(llm)
     result = pandas_ai.run(df,prompt=prompt)
     print(result)
     return result


def main():
    load_dotenv()
     # Load the OpenAI API key from the environment variable
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")

    st.set_page_config(page_title="AskCSV",page_icon=":robot:",layout="wide")
    
    #CSS
    hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    bg = """
        <style> [data-testid="stAppViewContainer"]
        {
            background: rgb(113,25,192);
            background: linear-gradient(90deg, rgba(113,25,192,0.9903420840992647) 5%, 
            rgba(41,59,181,1) 50%, rgba(143,0,255,1) 95%);
        }
        </style>
        """
    st.markdown(bg, unsafe_allow_html=True)
    
    st.header("Ask your CSV 💬")

    user_csv = st.file_uploader("Upload your CSV file", type ="csv")

    if user_csv is not None:
        col1,col2 = st.columns([1,1])
        with col1:
           #user_question = st.text_input("Ask a question about your CSV:")
            data = pd.read_csv(user_csv)
            st.dataframe(data)

        with col2:
            st.info("Chat with your CSV")

            input_text = st.text_input("Enter your Query")
            if input_text is not None:
                if st.button("Chat with CSV"):
                    st.info("Your query: "+input_text)
                    result = chat_with_csv(data,input_text)
                    st.success(result)

main()