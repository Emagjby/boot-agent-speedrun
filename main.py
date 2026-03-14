import argparse
import os
import sys

import google.genai.types as types
from dotenv import load_dotenv
from google import genai
from google.genai.types import Content, GenerateContentResponse, Part

from call_function import AVAILABLE_FUNCTIONS, call_function

SYSTEM_PROMPT = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


def load_api_key():
    _ = load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")
    return api_key


def parse_args() -> tuple[str, bool]:
    parser = argparse.ArgumentParser(description="Chatbot")
    _ = parser.add_argument(
        "user_prompt", type=str, help="The user's prompt to the chatbot"
    )
    _ = parser.add_argument(
        "--verbose", action="store_true", help="Enable verbose output"
    )
    args = parser.parse_args()
    return args.user_prompt, (True if args.verbose else False)


def prompt(client: genai.Client, messages: list[Content]) -> GenerateContentResponse:
    return client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[AVAILABLE_FUNCTIONS],
            system_instruction=SYSTEM_PROMPT,
            temperature=0,
        ),
    )


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


def _get_candidate_contents(res: GenerateContentResponse) -> list[Content]:
    if not res.candidates:
        return []

    contents = []
    for candidate in res.candidates:
        if candidate.content is not None:
            contents.append(candidate.content)

    return contents


def _get_function_calls(res: GenerateContentResponse):
    function_calls = []

    for content in _get_candidate_contents(res):
        for part in content.parts or []:
            if part.function_call:
                function_calls.append(part.function_call)

    return function_calls


def _print_text_response(res: GenerateContentResponse):
    response_text = (res.text or "").strip()
    if response_text:
        print(response_text)
        return

    for content in _get_candidate_contents(res):
        for part in content.parts or []:
            if part.text:
                print(part.text)


def main():
    api_key = load_api_key()
    user_prompt, verbose = parse_args()
    client = genai.Client(api_key=api_key)
    messages = [Content(role="user", parts=[Part(text=user_prompt)])]

    for _ in range(20):
        res = prompt(client, messages)

        if verbose:
            print_verbose(res, user_prompt)

        candidate_contents = _get_candidate_contents(res)
        for content in candidate_contents:
            messages.append(content)

        function_calls = _get_function_calls(res)
        if not function_calls:
            print("Final response:")
            _print_text_response(res)
            return

        function_responses = []
        for function_call in function_calls:
            function_call_result = call_function(function_call, verbose=verbose)

            if not function_call_result.parts:
                raise Exception("Function call result has no parts")

            function_response = function_call_result.parts[0].function_response
            if function_response is None:
                raise Exception("Function call result has no function_response")

            if function_response.response is None:
                raise Exception("Function response has no response payload")

            function_responses.append(function_call_result.parts[0])
            if verbose:
                print(f"-> {function_response.response}")

        messages.append(types.Content(role="user", parts=function_responses))

    print("Error: maximum iteration limit reached before final response.")
    sys.exit(1)


if __name__ == "__main__":
    main()
