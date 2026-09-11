import streamlit as st
from api_client import query_backend
from PIL import Image
import io

st.set_page_config(
    page_title="Set-Piece Tactical Analyzer",
    page_icon="⚽",
    layout="wide"
)

st.title("⚽ Set-Piece Tactical Analyzer (Multimodal RAG)")
st.markdown("Upload an image of a corner kick setup and ask tactical questions based on FIFA manuals.")

# Two columns layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Visual Context")
    uploaded_file = st.file_uploader("Upload Corner Kick Image (Optional)", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Setup", use_container_width=True)
        image_bytes = uploaded_file.getvalue()
        image_name = uploaded_file.name
    else:
        st.info("No image uploaded. The model will answer purely based on the text manuals.")
        image_bytes = None
        image_name = None

with col2:
    st.subheader("2. Tactical Chat")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Chat history container to keep input at the bottom
    chat_container = st.container(height=600)

    # Display chat messages from history on app rerun
    with chat_container:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
                if "sources" in message and message["sources"]:
                    st.caption(f"Sources: {', '.join(message['sources'])}")

    # React to user input
    if prompt := st.chat_input("Ask a tactical question... (e.g. How do we defend this?)"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message immediately in container
        with chat_container:
            with st.chat_message("user"):
                st.markdown(prompt)

        # Call backend
        with st.spinner("Analyzing image and retrieving tactical documents..."):
            response_data = query_backend(prompt, image_bytes, image_name)
            
            if "error" in response_data:
                response_text = response_data["error"]
                sources = []
            else:
                response_text = response_data.get("answer", "No answer received.")
                sources = response_data.get("sources", [])

        # Add assistant response to chat history
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response_text,
            "sources": sources
        })
        
        # Display assistant response immediately in container
        with chat_container:
            with st.chat_message("assistant"):
                st.markdown(response_text)
                if sources:
                    st.caption(f"Sources: {', '.join(sources)}")
