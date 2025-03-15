import streamlit as st
from grid_gen.grid_gen_bitmaps import ccw_csp
from content_mapping_gen import content_mapping_ui

def main():
    st.title("Crossword Go Tool")
    
    selected_option = st.selectbox(
        "Select Operation",
        ["Generate Grids", "Generate Content Mapping"],
        index=None,
        placeholder="Choose an operation..."
    )

    if selected_option == "Generate Grids":
        ccw_csp.main()
        
    elif selected_option == "Generate Content Mapping":
        content_mapping_ui.main()
        # Content mapping logic will go here

if __name__ == "__main__":
    main()
