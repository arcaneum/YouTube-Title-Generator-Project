# Import necessary libraries
import streamlit as st
from pydantic import BaseModel
from typing import List
import openai
# import os

# Access the API key from Streamlit Cloud Secrets
# This line retrieves the OpenAI API key stored in the Streamlit Cloud Secrets.
# It's essential for the app to authenticate with the OpenAI API.
openai_api_key = st.secrets["openai"]["OPENAI_API_KEY"]
# os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']

# Set the API key for OpenAI
# This sets the retrieved API key for use in all OpenAI API calls within the app.
openai.api_key = openai_api_key

# Pydantic model for structured data validation
class Titles(BaseModel):
    titles: List[str]

# Function to generate YouTube titles using OpenAI
def structured_generator(openai_model, prompt, custom_model):
    response = openai.ChatCompletion.create(
        model=openai_model, 
        prompt=prompt,
        max_tokens=100
    )
    return custom_model(titles=response.choices[0].text.strip().split('\n'))

# Streamlit UI layout starts here
st.title("YouTube Title Generator")

# Input field for topic
topic = st.text_input("Enter Topic")

# Button to generate titles
if st.button("Generate Titles"):
    if topic:
        try:
            prompt = f"Generate 5 creative YouTube title ideas for the topic: '{topic}'"
            openai_model = "gpt-3.5-turbo"
            result = structured_generator(openai_model, prompt, Titles)
            if result.titles:
                for title in result.titles:
                    st.write(title)
            else:
                st.error("No titles were generated. Try a different topic.")
        except Exception as e:
            st.error(f"Error in generating titles: {e}")
    else:
        st.error("Please enter a topic.")
