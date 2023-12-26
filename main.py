import streamlit as st
from pydantic import BaseModel
from typing import List
from openai import OpenAI  # Corrected import statement as per the latest OpenAI SDK

# Access the API key from Streamlit Cloud Secrets
OpenAI_api_key = st.secrets["openai"]["OPENAI_API_KEY"]

# Create an OpenAI client with the retrieved API key
client = OpenAI(api_key=OpenAI_api_key)

# Pydantic model for structured data validation
class Titles(BaseModel):
    titles: List[str]

# Function to generate YouTube titles using OpenAI
def structured_generator(openai_model, prompt, custom_model):
    # Prepare the conversation messages
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]

    # Make the API call to OpenAI using the chat completion endpoint
    response = client.chat.completions.create(
        model=openai_model, 
        messages=messages
    )

    # Parse the response to get the titles
    return custom_model(titles=response.choices[0].message['content'].strip().split('\n'))

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
