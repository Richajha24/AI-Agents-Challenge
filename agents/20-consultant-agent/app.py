import streamlit as st
from pathlib import Path
from groq_client import GroqClient

# Page configuration
st.set_page_config(
    page_title="Consultant Agent",
    page_icon="🎯",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 1rem;
    }
</style>
""", unsafe_allow_html=True)


def load_system_prompt() -> str:
    """Load the system prompt from the prompts directory."""
    prompt_path = Path(__file__).parent / "prompts" / "system_prompt.md"
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        st.error("Error: system_prompt.md not found in prompts directory")
        st.stop()


def main():
    """Main application for Consultant Agent."""
    # Header
    st.markdown('<p class="main-header">🎯 Consultant Agent</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-Powered Business Strategy Assistant</p>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    st.sidebar.header("About")
    st.sidebar.info("""
    This agent analyzes business challenges and generates structured consulting-style recommendations including:
    
    - Executive Summary
    - SWOT Analysis
    - Strategic Recommendations
    - Risk Assessment
    - Action Plan
    """)
    
    # Initialize session state
    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = None
    
    # Input section
    st.header("Business Challenge")
    st.subheader("Describe your business challenge or problem")
    
    business_challenge = st.text_area(
        "Enter your business challenge:",
        placeholder="Example: Our e-commerce company is experiencing declining customer retention rates over the past 6 months. We need to understand the root causes and develop a strategy to improve customer loyalty.",
        height=150
    )
    
    # Generate button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        generate_button = st.button("Generate Analysis", type="primary", use_container_width=True)
    
    # Generate analysis
    if generate_button:
        if not business_challenge.strip():
            st.error("Please enter a business challenge to analyze.")
        else:
            try:
                # Load system prompt
                system_prompt = load_system_prompt()
                
                # Initialize Groq client
                with st.spinner("Analyzing business challenge..."):
                    groq_client = GroqClient()
                    
                    # Generate consulting analysis
                    analysis = groq_client.generate_consulting_analysis(business_challenge, system_prompt)
                    
                    # Store in session state
                    st.session_state.analysis_result = analysis
                    
                    # Success message
                    st.markdown('<div class="success-box">✅ Analysis generated successfully!</div>', unsafe_allow_html=True)
                    
            except ValueError as e:
                st.error(f"Configuration Error: {str(e)}")
                st.error("Please ensure GROQ_API_KEY is set in your .env file")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # Display results
    if st.session_state.analysis_result:
        st.markdown("---")
        st.header("Consulting Analysis Results")
        
        # Display markdown
        st.markdown(st.session_state.analysis_result)
        
        # Download button
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.download_button(
                label="Download Analysis",
                data=st.session_state.analysis_result,
                file_name="consulting_analysis.md",
                mime="text/markdown",
                use_container_width=True
            )
        
        # Clear button
        if st.button("Clear Analysis"):
            st.session_state.analysis_result = None
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; font-size: 0.9rem;'>
    Consultant Agent • Powered by Groq API • Built with Streamlit
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()