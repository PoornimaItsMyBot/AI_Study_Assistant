import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import errors

load_dotenv()


class GeminiClient:
    """
    Low-level wrapper around the Gemini API. Its only job is sending a
    prompt to Gemini and returning the raw text response. It doesn't know
    anything about what the prompt says or how the response should be
    used — that logic lives in prompts.py and parser.py.
    """

    def __init__(self, model="gemini-3.5-flash", max_retries=3, retry_delay_seconds=5):
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found. Add it to your .env file.")

        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.max_retries = max_retries
        self.retry_delay_seconds = retry_delay_seconds

    def generate_text(self, prompt):
        """
        Sends a prompt to Gemini and returns the raw text response.
        Automatically retries a few times if Gemini's servers are
        temporarily overloaded (a 503 error), since this is usually
        short-lived and not caused by anything in our code.
        """
        last_error = None

        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt
                )
                return response.text.strip()

            except errors.ServerError as error:
                last_error = error
                print(f"Gemini server busy (attempt {attempt}/{self.max_retries}). Retrying...")
                time.sleep(self.retry_delay_seconds)

        # If every retry failed, raise a clear error instead of a raw traceback
        raise RuntimeError(
            f"Gemini API is currently unavailable after {self.max_retries} attempts. "
            f"Please try again in a few minutes. Original error: {last_error}"
        )
    #test pull