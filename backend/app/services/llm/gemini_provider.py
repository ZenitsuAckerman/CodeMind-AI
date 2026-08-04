from google import genai
from fastapi import HTTPException, status
from app.config.settings import settings

class GeminiProvider:
    """
    Communicates with the Google Gemini API using the official google-genai SDK.
    """
    def __init__(self):
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not configured in settings.")
        self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        self.model_name = 'gemini-1.5-flash'

    async def generate_answer(self, prompt: str) -> str:
        """
        Sends the final constructed prompt to Gemini and returns the response.
        """
        try:
            # Using the new async client interface
            response = await self.client.aio.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            return response.text
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Failed to communicate with Gemini API: {str(e)}"
            )

gemini_provider = GeminiProvider() if settings.GEMINI_API_KEY else None
