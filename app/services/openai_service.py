import time
import  openai

from openai import (
    OpenAIError,
    APIError,
    AuthenticationError,
    BadRequestError,
    RateLimitError,
    InternalServerError,
)
from flask import current_app


def get_openai_answer(question):
    """
    Get an AI-generated answer to a question using the OpenAI API.
    Handles errors, retries, and rate limits gracefully.

    Args:
        question (str): The user's question.

    Returns:
        str: The AI-generated answer or an appropriate error message.

    Raises:
        ValueError: If the API fails after retries or other unrecoverable errors occur.
    """
    openai.api_key = current_app.config.get("OPENAI_API_KEY")
    if not openai.api_key:
        raise ValueError("Missing OpenAI API key in configuration.")

    retry_count = 0
    max_retries = 5
    backoff_factor = 2

    while retry_count < max_retries:
        try:
            client = openai.OpenAI()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an all-knowing assistant. Answer the following question accurately.",
                    },
                    {"role": "user", "content": question},
                ],
                temperature=0.7,
            )
            return response.choices[0].message.content

        except AuthenticationError:
            current_app.logger.error("Authentication error: Invalid API key.")
            raise ValueError("Invalid API key for OpenAI.")

        except RateLimitError as e:
            retry_count += 1
            wait_time = backoff_factor ** retry_count
            current_app.logger.warning(
                f"Rate limit exceeded. Retrying in {wait_time} seconds. Error: {e}"
            )
            time.sleep(wait_time)

        except InternalServerError as e:
            retry_count += 1
            wait_time = backoff_factor ** retry_count
            current_app.logger.warning(
                f"Service unavailable. Retrying in {wait_time} seconds. Error: {e}"
            )
            time.sleep(wait_time)

        except APIError as e:
            current_app.logger.error(f"API error: {e}")
            raise ValueError("A server-side error occurred. Please try again later.")

        except BadRequestError as e:
            current_app.logger.error(f"Invalid request error: {e}")
            raise ValueError("Invalid request to the OpenAI API. Check your input.")

        except OpenAIError as e:
            current_app.logger.error(f"OpenAI error: {e}")
            raise ValueError("An error occurred while processing your request.")

        except Exception as e:
            current_app.logger.error(f"Unexpected error: {e}")
            raise ValueError("An unexpected error occurred. Please try again later.")
    current_app.logger.error("Max retries exceeded for OpenAI API.")
    raise ValueError("Unable to fetch a response from OpenAI after multiple attempts.")

