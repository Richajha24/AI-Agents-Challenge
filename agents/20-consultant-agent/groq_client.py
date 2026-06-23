import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class GroqClient:
    """Client for interacting with Groq API."""
    
    def __init__(self):
        """Initialize the Groq client with API key from environment."""
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.3-70b-versatile"
    
    def generate_response(self, system_prompt: str, user_message: str) -> str:
        """
        Generate a response from Groq API.
        
        Args:
            system_prompt: The system prompt to guide the AI's behavior
            user_message: The user's input message
            
        Returns:
            The generated response text
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.7,
                max_tokens=4096
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error generating response from Groq: {str(e)}")
    
    def generate_consulting_analysis(self, business_challenge: str, system_prompt: str) -> str:
        """
        Generate comprehensive consulting analysis based on business challenge.
        
        Args:
            business_challenge: The business challenge or problem to analyze
            system_prompt: The system prompt for the consultant agent
            
        Returns:
            Generated consulting analysis in markdown format
        """
        user_message = f"""Analyze the following business challenge and provide comprehensive consulting recommendations:

{business_challenge}

Please provide a complete analysis including:
1. Executive Summary
2. SWOT Analysis (Strengths, Weaknesses, Opportunities, Threats)
3. Strategic Recommendations
4. Risk Assessment
5. Action Plan with implementation steps and success metrics

Format the output in markdown with clear sections and bullet points."""
        
        return self.generate_response(system_prompt, user_message)