from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
from dotenv import load_dotenv
import os
import streamlit as st
import tempfile
import pandas as pd

OPENAI_API_KEY= st.secrets["auth_token"]

def main():
    #load_dotenv()
    st.set_page_config(page_title="AskCSV",page_icon=":robot:",layout="wide")

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
    
    st.header("Ask your CSV 📊")

    csv_file = st.file_uploader("Upload a CSV file", type="csv")
    if csv_file is not None:
        col1,col2 = st.columns([1,1])
        with col1:
        # Save the uploaded file to a temporary location
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_file.write(csv_file.read())
                csv_file_path = temp_file.name
            
            # Read the CSV file
            data = pd.read_csv(csv_file_path)

            # Display the data frame on the left side
            st.info("CSV Dataset")
            st.dataframe(data)
        
        with col2:

            st.info("Chat with your CSV")
            input_text = st.text_input("Enter your Query")
            if input_text is not None:
                if st.button("chat with csv"):
                    agent = create_csv_agent(OpenAI(temperature=0,openai_api_key="OPENAI_API_KEY"), csv_file_path, verbose=True)
                    with st.spinner(text="In progress..."):
                        st.info("Your query: "+input_text)
                        st.write(agent.run(input_text))


if __name__ == "__main__":
    main()
