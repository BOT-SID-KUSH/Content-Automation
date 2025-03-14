import streamlit as st
import base64
import io
import zipfile

import sys
import os
# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import src.grid_generator.grid_gen_bitmaps.ccw_csp as ccw_csp

def get_download_link(generated_grids):
    """Create a download link for the generated grids and clues TSV"""
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
        # Add grid files
        for filename, grid in generated_grids:
            grid_text = "\n".join(["".join(row) for row in grid])
            zip_file.writestr(f"grids/{filename}", grid_text)
        
        # Generate and add the clues TSV file
        tsv_content = generate_grid_clues_tsv(generated_grids)
        zip_file.writestr("grid_clues.tsv", tsv_content)
    
    zip_buffer.seek(0)
    b64 = base64.b64encode(zip_buffer.read()).decode()
    
    return f'<a href="data:application/zip;base64,{b64}" download="crossword_grids.zip">Download Crossword Grids</a>'

def render_grid_generator():
    st.title("Crossword Grid Generator")
    
    st.write("""
    This app generates filled crossword grids using a constraint satisfaction algorithm.
    Please upload a previous content file to begin.
    """)
    
    # Add file uploader for previous_content.tsv
    st.subheader("Upload previous content")
    st.write("Please upload a previous_content.tsv file to continue.")
    uploaded_file = st.file_uploader("Upload previous_content.tsv", type=["tsv"])
    
    if uploaded_file is not None:
        previous_content = uploaded_file.read()
        st.success("File uploaded successfully!")
        start_puzzle_num = st.number_input("Start puzzle number", value=None, min_value=1, max_value=1000000, step=1)
        
        if start_puzzle_num:
            st.write(f"Starting from puzzle number: {start_puzzle_num}")
            st.write("""
            Select the number of puzzles to generate and click the button below.
            """)
            
            num_puzzles = st.slider("Number of puzzles to generate", 1, 200, 20)
            use_quick = True
            
            if st.button("Generate Crossword Grids"):
                generated_grids = fill_grid_completely(start_puzzle_num, num_puzzles, use_quick, previous_content)
                
                if generated_grids:
                    st.success(f"Successfully generated {len(generated_grids)} crossword grids!")
                    
                    # Provide download link
                    st.markdown(get_download_link(generated_grids), unsafe_allow_html=True)

                    # Display a sample of the generated grids
                    st.subheader("Sample of Generated Grids")
                    for i, (filename, grid) in enumerate(generated_grids):
                        with st.expander(f"Grid {i+1} - {filename}"):
                            st.markdown(display_grid(grid), unsafe_allow_html=True)
                else:
                    st.warning("No grids were generated. Try again or adjust parameters.")
        else:
            st.warning("Please enter a starting puzzle number")

if __name__ == "__main__":
    render_grid_generator()
