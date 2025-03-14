import streamlit as st
import json
import io
import base64
from src.content_mapping.content_mapping import extract_content_mapping


# TODO:
# flow
# - user will get an option to upload the files 
# - dummy json format will be in the backend and this will be visible to to the user.
# - after user uploads , an option to edit the colum number will be given.
# - after editing , an option to download the content mapping will be given.
# - user have to put the version number.
# - after clicking on download button , the content mapping will be downloaded in the json format.

def render_content_mapping():
    # Create a layout with two columns at the top
    col1, col2 = st.columns([2, 1])  # 2:1 ratio for left:right columns
    
    # Main content in the left column
    with col1:
        
        # Input fields for version numbers
        version = st.number_input("Enter v (Version Number)", min_value=1, step=1)
        
        # File uploader for TSV file
        uploaded_file = st.file_uploader("Upload TSV file", type=['tsv'])
        content = None
    
    # Example format in the right column
    with col2:
        st.subheader("Format : ")
        with open('src/content_mapping/format.json', 'r') as f:
            example_format = json.load(f)
        st.json(example_format)
    
    # Continue with the rest of the content below the columns
    if uploaded_file is not None:
        # Display success message
        st.success("File uploaded successfully!")
        content = uploaded_file.read().decode('utf-8')

    if st.button("Generate"):
        with st.spinner("Generating content mapping..."):
            # Generate the JSON content
            content = extract_content_mapping(content,version)
            
            # Convert to JSON string
            json_str = json.dumps(content)
            
            # Create download button
            b64 = base64.b64encode(json_str.encode()).decode()
            href = f'<a href="data:application/json;base64,{b64}" download="content_mapping.json">Download JSON</a>'
            st.markdown(href, unsafe_allow_html=True)
            
            # Also display the JSON in a scrollable window
            st.markdown("""
                <div style="height: 300px; overflow-y: scroll; border: 1px solid #ccc; padding: 10px;">
                    <pre>{}</pre>
                </div>
                """.format(json.dumps(content, indent=2)), unsafe_allow_html=True)

    st.markdown("---")

    
   

    
