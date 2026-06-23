from __future__ import annotations

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

from groq_client import generate


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
SYSTEM_PROMPT_PATH = BASE_DIR / "prompts" / "system_prompt.md"
OUTPUT_PATH = BASE_DIR / "trend_report.md"


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def _build_user_input(industry: str, time_horizon: str, region: str | None) -> str:
    region_part = region.strip() if region else "Global"
    return (
        f"Industry/Topic: {industry.strip()}\n"
        f"Time Horizon: {time_horizon.strip()}\n"
        f"Region: {region_part}\n\n"
        "Please produce the trend analysis report using the required sections."
    )


def main() -> None:
    st.set_page_config(page_title="Trend Discovery", layout="wide")

    st.title("Trend Discovery")
    st.caption("Identify emerging trends and turn them into strategic business insights.")

    with st.form("trend_form"):
        industry = st.text_input("Industry / Topic", value="Artificial Intelligence")
        time_horizon = st.selectbox(
            "Time Horizon",
            options=["6 Months", "1 Year", "3 Years", "5 Years"],
            index=2,
        )
        region = st.text_input("Region (optional)", value="Global")

        submitted = st.form_submit_button("Generate report")

    if not submitted:
        return

    if not SYSTEM_PROMPT_PATH.exists():
        st.error(f"System prompt missing: {SYSTEM_PROMPT_PATH}")
        return

    system_prompt = _read_text(SYSTEM_PROMPT_PATH)
    user_input = _build_user_input(industry, time_horizon, region)

    with st.spinner("Analyzing trends with Groq..."):
        try:
            report = generate(system_prompt=system_prompt, user_input=user_input)
        except Exception as e:
            st.error(str(e))
            return

    st.subheader("Report")
    st.markdown(report)

    # Save to disk
    OUTPUT_PATH.write_text(report, encoding="utf-8")
    st.success(f"Saved report to: {OUTPUT_PATH.name}")


if __name__ == "__main__":
    main()

