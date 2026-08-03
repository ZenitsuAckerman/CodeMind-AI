import google.generativeai as genai
from fastapi import HTTPException, status
from app.config.settings import settings

class GeminiProvider:
    """
    Communicates with the Google Gemini API.
    """
    def __init__(self):
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY is not configured in settings.")
        genai.configure(api_key=settings.GEMINI_API_KEY)
        # Use gemini-1.5-flash for fast, concise responses
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    async def generate_answer(self, prompt: str) -> str:
        """
        Sends the final constructed prompt to Gemini and returns the response.
        """
        try:
            # Using generate_content_async for non-blocking I/O
            response = await self.model.generate_content_async(prompt)
            return response.text
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Failed to communicate with Gemini API: {str(e)}"
            )

gemini_provider = GeminiProvider() if settings.GEMINI_API_KEY else None
