import streamlit as st
import pdfplumber

# Logic to upload and store resume data 
st.title('PDF File Upload Example')

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
            st.subheader(f'Page {page_num + 1}')
            st.write(page_text if page_text else "No text found on this page.")
