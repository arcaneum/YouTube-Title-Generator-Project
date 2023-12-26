import streamlit as st
from pydantic import BaseModel
from typing import List
import openai

# Access the API key from Streamlit Cloud Secrets
openai_api_key = st.secrets['openai']["OPENAI_API_KEY"]

# Set the API key for OpenAI
openai.api_key = openai_api_key

# Assuming the patch function is defined in the instructor module
import instructor
instructor.patch(open_ai_client)

# Pydantic model for structured data validation
class Titles(BaseModel):
    titles: List[str]

# Function to generate YouTube titles using structured_generator
def structured_generator(openai_model, prompt, custom_model):
    result: custom_model = open_ai_client.chat.completions.create(
        model=openai_model, 
        response_model=custom_model,
        messages=[{"role": "user", "content": f"{prompt}, output must be in json"}]
    )
    return result

# Streamlit app layout
st.title("YouTube Title Generator")

# Input field for topic
topic = st.text_input("Enter Topic")

# Button to generate titles
if st.button("Generate Titles"):
    if topic:
        try:
            # Call function to generate titles
            prompt = f"Generate 5 creative YouTube title ideas for the topic: '{topic}'"
            openai_model = "gpt-3.5-turbo"
            result = structured_generator(openai_model, prompt, Titles)
            # Displaying titles
            if result.titles:
                for title in result.titles:
                    st.write(title)
            else:
                st.error("No titles were generated. Try a different topic.")
        except Exception as e:
            st.error(f"Error in generating titles: {e}")
    else:
        st.error("Please enter a topic.")
