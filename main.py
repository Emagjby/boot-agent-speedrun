import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai.types import Content, GenerateContentResponse, Part


def load_api_key():
    _ = load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")
    return api_key


def parse_args() -> str:
    parser = argparse.ArgumentParser(description="Chatbot")
    _ = parser.add_argument(
        "user_prompt", type=str, help="The user's prompt to the chatbot"
    )
    _ = parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose output"
    )
    args = parser.parse_args()
    return args.user_prompt, (True if args.verbose else False)


def prompt(api_key: str, user_prompt: str) -> GenerateContentResponse:
    message = [Content(role="user", parts=[Part(text=user_prompt)])]

    client = genai.Client(api_key=api_key)
    res = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=message,
    )

    return res


def print_verbose(res: GenerateContentResponse, user_prompt: str):
    def print_token_usage():
        if res.usage_metadata is None:
            raise Exception("Usage Metadata is None")

        print("\n")
        print("Prompt tokens: ", res.usage_metadata.prompt_token_count)
        print("Response tokens: ", res.usage_metadata.candidates_token_count)
        print("\n")

    def print_user_prompt():
        print("\n")
        print("User prompt: ", user_prompt)

    print_user_prompt()
    print_token_usage()


def print_response(res: GenerateContentResponse):
    print(res.text)


def main():
    api_key = load_api_key()
    get_user_prompt, verbose = parse_args()

    res = prompt(api_key, get_user_prompt)

    if verbose:
        print_verbose(res, get_user_prompt)

    print_response(res)


if __name__ == "__main__":
    main()
