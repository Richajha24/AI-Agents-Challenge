# Newsletter Agent

A Streamlit web app that generates professional newsletters instantly using AI.

## Stack
- Python 3.12
- Streamlit
- Groq API (model: llama-3.3-70b-versatile)
- python-dotenv

## Setup

1. Clone the repository and navigate to the `agent-15-newsletter-agent` directory.

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

1. Enter your newsletter topic in the text area.
2. Specify the target audience (e.g., startup founders, college students).
3. Select the tone: Professional, Casual, Inspirational, or Educational.
4. Choose the number of sections (default: 4).
5. Click "Generate Newsletter" to create your newsletter.
6. Review the generated newsletter and download it as a markdown file.
