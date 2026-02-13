import streamlit as st
import random
import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Lab 1 - Echo Chat", page_icon="💬")
st.title("💬 Echo Chat")

#Calling api_key:
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("The api key is missing.")
    st.stop

genai.configure(api_key=api_key)


model  = genai.GenerativeModel("gemini-2.5-flash")
                            
# def echo_greet():
#     salutations =["Greet the user with a small casual sentence or two.", 
#                   "Make sure to include a different emoji for each and every response.",
#                   "Make sure to use a different sentence each time."
#                   "Make sure to ONLY greet the user. NO extra texts!"]
    
#     response = model.generate_content(salutations)
    # return response.text




if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I echo you."}
    ]

   

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

prompt = st.chat_input("Say something")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # greet = echo_greet()
    response = model.generate_content(prompt)

    st.session_state.messages.append({"role": "assistant", "content": f"{response.text}" })

    st.rerun()
