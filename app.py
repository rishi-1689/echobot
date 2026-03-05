import streamlit as st
import random
import os

from dotenv import load_dotenv
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity 
load_dotenv()

st.set_page_config(page_title="Lab 1 - Echo Chat", page_icon="💬")
st.title("💬 Echo Chat")

# testing if module works:
try:
    import google.generativeai as genai
    st.sidebar.success("google.generativeai imported ✅")
except Exception as e:
    st.sidebar.error(f"Failed to import google.generativeai: {e!r}")
    st.stop()

# extracting text:
def pdf_extract_text(uploaded_file) -> str:
    reader = PdfReader(uploaded_file)
    return "\n\n".join([(p.extract_text() or "") for p in reader.pages])

# turning extracted texts into chunks:
def chunk_text(text, chunk_size=1200, overlap=200):
    chunks=[]
    start=0
    while start<len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
            start = end - overlap
            if end == len(text):
                break
    return chunks

def build_tfidf_index(chunks):
    vec = TfidfVectorizer(
        ngram_range=(1,2),
        min_df=1
    )

    X =vec.fit_transform(chunks)
    return vec, X

def retrieve_top_k(query, chunks, vec, X, k=4):
    Q = vec.transform([query])
    scores = cosine_similarity(Q, X)[0]
    top_score = scores.argsort()[::-1][:k]
    return[(int(i), float(scores[i]), chunks[int[i]]) for i in top_score]




# Setting Presets:
PRESETS= {"Trainer-Guy":"You are a motivational trainer.",
          "Poet":"You are an artistic poet.",
          "Geek":"You are an enthsiastic geek, who loves to elaborate and stretch his answers as long as possible.",
          "German-fella":"You are a helpful assistant who gives all his answers in German."}

# Customzing sidebar:
st.sidebar.header("My Personalities.")

selected_preset = st.sidebar.selectbox("Choose One: ",
                                         list(PRESETS.keys()),
                                         index=0)


# upload pdf:
st.sidebar.header("Upload a PDF")

uploaded_pdf = st.sidebar.file_uploader(
    "Upload a PDF document",
    type=["pdf"]
)

# Making your own:
use_custom = st.sidebar.toggle("Create your own custom personality.", value=False)


custom_instruction=""
if use_custom:
    custom_instruction = st.sidebar.text_area("Your instructions please.")

system_instruction = custom_instruction.strip() if use_custom else PRESETS[selected_preset]


# Added reruns:
if st.sidebar.button("Reset Chat"):
    st.session_state.messages = [
        {"role":"assistant", "content":"Hi! I echo you."}
    ]
    st.rerun()

#Calling api_key:
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    api_key = st.secrets.get("GEMINI_API_KEY")
if not api_key:
    st.error("The api key is missing.")
    st.stop

genai.configure(api_key=api_key)


model  = genai.GenerativeModel("gemini-2.5-flash",
                               system_instruction=system_instruction)
                            
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
