import streamlit as st
from ui.pages.grid_generator import render_grid_generator
from ui.pages.content_mapping import render_content_mapping
def main():
    st.title("Crossword Go Tool")
    
    selected_option = st.selectbox(
        "Select Operation",
        ["Generate Grids", "Generate Content Mapping"],
        index=None,
        placeholder="Choose an operation..."
    )

    if selected_option == "Generate Grids":
        render_grid_generator()
        
    elif selected_option == "Generate Content Mapping":
        st.write("Content Mapping Generator") 
        render_content_mapping()
        # Content mapping logic will go here

if __name__ == "__main__":
    main()
