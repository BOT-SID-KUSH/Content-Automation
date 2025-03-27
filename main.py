import streamlit as st
from ui.grid_generator.ccw_csp import main as ccw_csp_main
from ui.content_mapping.content_mapping_ui import main as content_mapping_ui_main

def main():
    st.title("Crossword Go Tool")
    
    selected_option = st.selectbox(
        "Select Operation",
        ["Generate Grids", "Generate Content Mapping"],
        index=None,
        placeholder="Choose an operation..."
    )

    if selected_option == "Generate Grids":
        ccw_csp_main()
        
    elif selected_option == "Generate Content Mapping":
        content_mapping_ui_main()
        # Content mapping logic will go here

if __name__ == "__main__":
    main()
