import streamlit as st
from groq_client import generate
import pathlib

# --- Page Config ---
st.set_page_config(
    page_title="Content Factory",
    page_icon="🏭",
    layout="wide"
)

# --- Load System Prompt ---
system_prompt = pathlib.Path("prompts/system_prompt.md").read_text()

# --- Header ---
st.title("🏭 Content Factory")
st.markdown("**Generate blogs, social posts, emails, and marketing copy — instantly.**")
st.divider()

# --- Input Section ---
col1, col2 = st.columns(2)

with col1:
    content_type = st.selectbox(
        "Content Type",
        options=[
            "Blog Post",
            "LinkedIn Post",
            "Twitter/X Thread",
            "Instagram Caption",
            "Marketing Email",
            "Product Description"
        ]
    )
    topic = st.text_input(
        "Topic / Subject",
        placeholder="e.g. How AI is changing hiring in India, VerifyU product launch, 5 habits of top students"
    )
    target_audience = st.text_input(
        "Target Audience",
        placeholder="e.g. College students, startup founders, HR managers"
    )

with col2:
    tone = st.selectbox(
        "Tone",
        options=[
            "Professional",
            "Casual & Conversational",
            "Inspirational",
            "Educational",
            "Witty & Humorous",
            "Bold & Provocative"
        ]
    )
    brand_name = st.text_input(
        "Brand / Product Name (optional)",
        placeholder="e.g. VerifyU, InternBot, MyStartup"
    )
    goal = st.selectbox(
        "Content Goal",
        options=[
            "Build Awareness",
            "Drive Engagement",
            "Generate Leads",
            "Educate Audience",
            "Announce a Product/Feature",
            "Build Personal Brand"
        ]
    )

key_points = st.text_area(
    "Key Points to Cover (optional)",
    placeholder="e.g. mention our free tier, highlight student verification feature, include India market stats...",
    height=80
)

# --- Generate Button ---
st.divider()
generate_btn = st.button("🚀 Generate Content", use_container_width=True, type="primary")

# --- Output ---
if generate_btn:
    if not topic or not target_audience:
        st.warning("Please enter a topic and target audience.")
    else:
        user_input = f"""
Content Type: {content_type}
Topic: {topic}
Target Audience: {target_audience}
Tone: {tone}
Brand/Product: {brand_name if brand_name else "Not specified"}
Goal: {goal}
Key Points to Cover: {key_points if key_points else "None provided"}

Generate the content now.
"""

        with st.spinner(f"Writing your {content_type}..."):
            try:
                result = generate(system_prompt, user_input)

                st.success(f"✅ {content_type} generated!")
                st.divider()

                # Show character count for social posts
                if content_type in ["Twitter/X Thread", "Instagram Caption", "LinkedIn Post"]:
                    st.caption(f"📊 Character count: {len(result)}")

                st.markdown(result)

                st.divider()
                file_name = f"{content_type.lower().replace('/', '_').replace(' ', '_')}_{topic[:30].lower().replace(' ', '_')}.md"
                st.download_button(
                    label=f"📥 Download {content_type} as Markdown",
                    data=result,
                    file_name=file_name,
                    mime="text/markdown",
                    use_container_width=True
                )

            except Exception as e:
                st.error(f"Error generating content: {str(e)}")
                st.info("Make sure your GROQ_API_KEY is set correctly in your .env file.")

# --- Footer ---
st.divider()
st.caption("Agent 18 — Content Factory | Powered by Groq + Llama 3.3 70B")