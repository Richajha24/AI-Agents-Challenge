# PRD Generator

A Streamlit web app that turns your product idea into a full Product Requirements Document using AI.

## Stack
- Python 3.12
- Streamlit
- Groq API (model: llama-3.3-70b-versatile)
- python-dotenv

## Setup

1. Clone the repository and navigate to the `agent-17-prd-generator` directory.

2. Create a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your Groq API key:
   - Copy `.env.example` to `.env`
   - Add your Groq API key to the `.env` file:
     ```
     GROQ_API_KEY=your_actual_api_key_here
     ```

5. Run the app:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Enter your product idea in the text area.
2. Optionally specify the target audience and problem it solves.
3. Click "Generate PRD" to create your Product Requirements Document.
4. Review the generated PRD and download it as a markdown file.
