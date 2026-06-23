import streamlit as st

from groq_client import GroqClient


def build_system_prompt_path() -> str:
    # system_prompt is imported by GroqClient
    return ""


def main() -> None:
    st.set_page_config(page_title="Sales Agent", layout="centered")

    st.title("Sales Agent")
    st.subheader("AI-powered sales assistant and outreach generator")

    product_service = st.text_area("Your Product/Service", height=140, placeholder="What are you selling?")
    target_customer = st.text_input("Target Customer", placeholder="e.g. SaaS startups, D2C brands")

    outreach_type = st.selectbox(
        "Outreach Type",
        options=["Cold Email", "LinkedIn Message", "Follow-up Email", "Sales Pitch Script"],
    )

    pain_point = st.text_input("Key Pain Point to Address", placeholder="e.g. slow onboarding, low retention")

    tone = st.selectbox("Tone", options=["Professional", "Friendly", "Urgent", "Consultative"])

    if st.button("Generate Sales Content", type="primary"):
        if not product_service.strip() or not target_customer.strip() or not pain_point.strip():
            st.error("Please fill in: Your Product/Service, Target Customer, and Key Pain Point to Address.")
            return

        client = GroqClient()

        user_input = (
            f"Product/Service: {product_service}\n"
            f"Target Customer: {target_customer}\n"
            f"Outreach Type: {outreach_type}\n"
            f"Key Pain Point: {pain_point}\n"
            f"Tone: {tone}\n"
            "\nGenerate clean markdown only."
        )

        with st.spinner("Generating sales content..."):
            try:
                system_prompt = client.load_system_prompt()
                result_md = client.generate(system_prompt=system_prompt, user_input=user_input)
            except Exception as exc:
                st.error(f"Generation failed: {exc}")
                return

        st.markdown(result_md)

        filename = "Sales_generated.md"
        st.download_button(
            label="Download",
            data=result_md.encode("utf-8"),
            file_name=filename,
            mime="text/markdown",
        )


if __name__ == "__main__":
    main()

