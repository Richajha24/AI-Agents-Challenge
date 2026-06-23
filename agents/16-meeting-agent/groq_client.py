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
    
    def generate_meeting_materials(self, meeting_context: str, system_prompt: str) -> str:
        """
        Generate comprehensive meeting materials based on context.
        
        Args:
            meeting_context: The context or topic of the meeting
            system_prompt: The system prompt for the meeting agent
            
        Returns:
            Generated meeting materials in markdown format
        """
        user_message = f"""Generate comprehensive meeting materials for the following meeting context:

{meeting_context}

Please provide:
1. Meeting Agenda with objectives and time allocations
2. Key Discussion Points
3. Risks and Blockers
4. Important Questions to Address
5. Action Items with responsibilities
6. Follow-up Recommendations

Format the output in markdown."""
        
        return self.generate_response(system_prompt, user_message)