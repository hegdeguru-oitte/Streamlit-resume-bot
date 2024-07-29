import streamlit as st
import pdfplumber
import replicate
import os

# App title
st.set_page_config(page_title="Llama 2 Resumebot")

# Replicate Credentials
with st.sidebar:
    st.title('🦙💬 Llama 2 Resumebot')
    st.write('This is a resume bot created using Llama 2 LLM to summarize resumes.')

    # Replicate Credentials
    replicate_api = st.text_input('Enter Replicate API token:', type='password')
    if not (replicate_api.startswith('r8_') and len(replicate_api)==40):
        st.warning('Please enter your credentials!', icon='⚠️')
    else:
        st.success('Proceed to entering your prompt message!', icon='👉')
    os.environ['REPLICATE_API_TOKEN'] = replicate_api
    
    # LLM Model chosen is 7B
    llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    # Parameters
    temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=1.0, value=0.1, step=0.01)
    top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.sidebar.slider('max_length', min_value=32, max_value=128, value=120, step=8)

    # Resume PDF Upload
    st.title('Upload your resume')
    resume=''

    # File upload widget
    uploaded_file = st.file_uploader("Choose a PDF file", type='pdf')

    if uploaded_file is not None:
        # Display file details
        st.write("Filename: ", uploaded_file.name)
        st.write("File type: ", uploaded_file.type)
        st.write("File size: ", uploaded_file.size, "bytes")
    
        # Open the PDF file using pdfplumber
        with pdfplumber.open(uploaded_file) as pdf:
            # Extract text from each page and display it
            for page_num, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                resume=page_text
                # st.subheader(f'Page {page_num + 1}')
                # st.write(page_text if page_text else "No text found on this page.")

if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)


# Function for generating LLaMA2 response. Refactored from https://github.com/a16z-infra/llama2-chatbot
def generate_llama2_response(prompt_input):
    string_dialogue = f"""
                    You are a resume summarizer. You will have to summarize the resume or need to answer questions based on the given resume.
                    You first greet the recruiter, then ask them if the would like a summary of the resume or if they have any particular requirements, \
                    If their requirement is found in the resume, you tell them about the experience and projects if any.
                    Below is the resume , delimited by triple 
                    backticks. If resume is null, request them to upload a resume.

                    Review: ```{resume}```


                    """

    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    output = replicate.run('a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea',input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ",
                                  "temperature":temperature, "top_p":top_p, "max_length":max_length, "repetition_penalty":1})
    return output


# User-provided prompt
if prompt := st.chat_input(disabled=not replicate_api):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_llama2_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)