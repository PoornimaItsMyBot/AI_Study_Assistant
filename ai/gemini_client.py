import os
import sys
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors


# Find the folder where the application is running
if getattr(sys, "frozen", False):
    # Running as a PyInstaller .exe
    app_folder = os.path.dirname(sys.executable)
else:
    # Running normally with Python
    app_folder = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )


# Look for .env in the application folder
env_path = os.path.join(app_folder, ".env")

load_dotenv(env_path)


class GeminiClient:
    """
    Low-level wrapper around the Gemini API.

    Its job is to send a prompt to Gemini
    and return the text response.
    """

    def __init__(
        self,
        model="gemini-3.5-flash",
        max_retries=3,
        retry_delay_seconds=5
    ):
        api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY not found. "
                "Add it to your .env file."
            )

        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.max_retries = max_retries
        self.retry_delay_seconds = retry_delay_seconds

    def generate_text(self, prompt):
        """
        Sends a prompt to Gemini and returns the raw text response.
        Automatically retries if Gemini's servers are temporarily busy.
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

                print(
                    f"Gemini server busy "
                    f"(attempt {attempt}/{self.max_retries}). "
                    f"Retrying..."
                )

                time.sleep(self.retry_delay_seconds)

        raise RuntimeError(
            f"Gemini API is currently unavailable after "
            f"{self.max_retries} attempts. "
            f"Please try again in a few minutes. "
            f"Original error: {last_error}"
        )