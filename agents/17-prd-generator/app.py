import streamlit as st
from groq_client import generate
import os

st.set_page_config(page_title="PRD Generator", page_icon="📝")

st.title("PRD Generator")
st.subheader("Turn your product idea into a full Product Requirements Document")

product_idea = st.text_area("Product Idea", height=150, placeholder="Describe your product idea in detail...")
target_audience = st.text_input("Target Audience", placeholder="Who is this product for?")
problem_solves = st.text_input("Problem it solves", placeholder="What problem does this product solve?")

if st.button("Generate PRD"):
    if not product_idea:
        st.error("Please enter a product idea.")
    else:
        with st.spinner("Generating PRD..."):
            # Load system prompt
            with open("prompts/system_prompt.md", "r") as f:
                system_prompt = f.read()
            
            # Build user input
            user_input = f"""Product Idea: {product_idea}
Target Audience: {target_audience}
Problem it solves: {problem_solves}"""
            
            # Generate PRD
            prd = generate(system_prompt, user_input)
            
            # Display result
            st.markdown(prd)
            
            # Store in session state for download
            st.session_state.generated_prd = prd

# Download button
if "generated_prd" in st.session_state:
    st.download_button(
        label="Download PRD",
        data=st.session_state.generated_prd,
        file_name="PRD_generated.md",
        mime="text/markdown"
    )
