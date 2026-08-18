import os
import sys
import time

from dotenv import load_dotenv
from google import genai
from google.genai import errors


def get_api_key():
    """
    Gets the Google Gemini API key.

    Priority:
    1. Streamlit Secrets when running on Streamlit Cloud
    2. .env when running locally or as a PyInstaller EXE
    """

    # =========================================================
    # OPTION 1: STREAMLIT CLOUD
    # =========================================================

    try:
        import streamlit as st

        if "GOOGLE_API_KEY" in st.secrets:

            api_key = st.secrets["GOOGLE_API_KEY"]

            if api_key:
                return api_key

    except Exception:
        # Streamlit is not available or secrets are not configured.
        # Continue to the .env method.
        pass

    # =========================================================
    # OPTION 2: LOCAL PYTHON / PYINSTALLER EXE
    # =========================================================

    if getattr(sys, "frozen", False):
        # Running as a PyInstaller EXE

        app_folder = os.path.dirname(
            sys.executable
        )

    else:
        # Running normally with Python

        app_folder = os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)
            )
        )

    env_path = os.path.join(
        app_folder,
        ".env"
    )

    load_dotenv(env_path)

    api_key = os.getenv(
        "GOOGLE_API_KEY"
    )

    return api_key


class GeminiClient:
    """
    Low-level wrapper around the Gemini API.

    Supports:

    Local Python:
        .env

    PyInstaller EXE:
        .env next to the EXE

    Streamlit Cloud:
        st.secrets
    """

    def __init__(
        self,
        model="gemini-3.5-flash",
        max_retries=3,
        retry_delay_seconds=5
    ):

        api_key = get_api_key()

        if not api_key:

            raise ValueError(
                "GOOGLE_API_KEY not found. "
                "For local/EXE use, add it to "
                "a .env file. "
                "For Streamlit Cloud, add it "
                "to Streamlit Secrets."
            )

        self.client = genai.Client(
            api_key=api_key
        )

        self.model = model

        self.max_retries = max_retries

        self.retry_delay_seconds = (
            retry_delay_seconds
        )

    def generate_text(self, prompt):
        """
        Sends a prompt to Gemini and returns
        the raw generated text.

        Retries automatically if Gemini
        temporarily returns a server error.
        """

        last_error = None

        for attempt in range(
            1,
            self.max_retries + 1
        ):

            try:

                response = (
                    self.client.models.generate_content(
                        model=self.model,
                        contents=prompt
                    )
                )

                return response.text.strip()

            except errors.ServerError as error:

                last_error = error

                print(
                    f"Gemini server busy "
                    f"(attempt {attempt}/"
                    f"{self.max_retries}). "
                    f"Retrying..."
                )

                time.sleep(
                    self.retry_delay_seconds
                )

        raise RuntimeError(
            f"Gemini API is currently unavailable "
            f"after {self.max_retries} attempts. "
            f"Please try again in a few minutes. "
            f"Original error: {last_error}"
        )