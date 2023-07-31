import streamlit as st
import pandas as pd
from langchain.agents import create_csv_agent
from langchain.llms import OpenAI
from dotenv import load_dotenv
import os
import tempfile
import numpy as np
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report

def main():
    load_dotenv()

    # Load the OpenAI API key from the environment variable
    if os.getenv("OPENAI_API_KEY") is None or os.getenv("OPENAI_API_KEY") == "":
        print("OPENAI_API_KEY is not set")
        exit(1)
    else:
        print("OPENAI_API_KEY is set")

    st.set_page_config(page_title="AskyourCSV", page_icon=":robot:", layout="wide")

    # CSS
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
            background: rgb(33, 36, 38);
        }
        </style>
        """
    st.markdown(bg, unsafe_allow_html=True)
    # Add the yellow top bar
    top_bar_html = """
    <style>
    .top-bar {
        background-color: #FFA500;
        padding: 10px 0;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        text-align: left;
        font-family: 'Russo One';
        font-size: 20px;
    }
    </style>
    <div class="top-bar">
        <span style="color: white ; font-weight: bold; padding-left: 80px;">The Techie Indian</span> 
    </div>
    """
    st.markdown(top_bar_html, unsafe_allow_html=True)

    #st.header("Ask your CSV")
    st.markdown("<h1 style='text-align: center; font-family:Abril Fatface ; -webkit-text-stroke: 1px yellow ;font-size: 60px; padding-bottom: 15px; color: rgb(255, 255, 255) ;'>Ask Your CSV</h1>", unsafe_allow_html=True)

    csv_file = st.file_uploader("Upload a CSV file", type="csv")
    if csv_file is not None:
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(csv_file.read())
            csv_file_path = temp_file.name

        # Read the CSV file
        data = pd.read_csv(csv_file_path)
        df = pd.DataFrame(csv_file)
        # Display the data frame
        st.subheader("CSV Data")
        st.dataframe(data)
        #pandas profiling report
        if st.button("Show Exploratory Data Analysis Report"):
            pr = ProfileReport(data,explorative=True,minimal=True)
            st.header("Pandas Profiling Report")
            st_profile_report(pr)
        #chatcsv
        st.info("Chat with your CSV")
        input_text = st.text_input("Enter your Query")
        if input_text is not None:
            if st.button("Chat with CSV"):
                agent = create_csv_agent(OpenAI(temperature=0), csv_file_path, verbose=True)
                with st.spinner(text="In progress..."):
                    st.info("Your query: " + input_text)
                    st.write(agent.run(input_text))


if __name__ == "__main__":
    main()
