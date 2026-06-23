import streamlit as st
from groq_client import generate
import os

st.set_page_config(page_title="Newsletter Agent", page_icon="📧")

st.title("Newsletter Agent")
st.subheader("Generate professional newsletters instantly")

newsletter_topic = st.text_area("Newsletter Topic", height=150, placeholder="Describe your newsletter topic in detail...")
target_audience = st.text_input("Target Audience", placeholder="e.g. startup founders, college students")
tone = st.selectbox("Tone", ["Professional", "Casual", "Inspirational", "Educational"])
num_sections = st.number_input("Number of Sections", min_value=1, max_value=10, value=4)

if st.button("Generate Newsletter"):
    if not newsletter_topic:
        st.error("Please enter a newsletter topic.")
    else:
        with st.spinner("Generating newsletter..."):
            # Load system prompt
            with open("prompts/system_prompt.md", "r") as f:
                system_prompt = f.read()
            
            # Build user input
            user_input = f"""Newsletter Topic: {newsletter_topic}
Target Audience: {target_audience}
Tone: {tone}
Number of Sections: {num_sections}"""
            
            # Generate newsletter
            newsletter = generate(system_prompt, user_input)
            
            # Display result
            st.markdown(newsletter)
            
            # Store in session state for download
            st.session_state.generated_newsletter = newsletter

# Download button
if "generated_newsletter" in st.session_state:
    st.download_button(
        label="Download Newsletter",
        data=st.session_state.generated_newsletter,
        file_name="Newsletter_generated.md",
        mime="text/markdown"
    )
