import sys
from functools import partial

from openai import OpenAI

from utils.error_handler import exception_log_message
from utils.logger import setup_logger

# Create a logger specific to this module
logger = setup_logger('OpenAIClient')


class OpenAIClient:

    def __init__(self, model,
                 num_requests=1,
                 temperature=1.0, response_format=None,
                 tools=None, tool_choice="auto",
                 parallel_tool_calls=False):

        client_kwargs = {
            "model": model,
            "n": num_requests,
            "max_completion_tokens": 5000,
            "response_format": response_format
        }

        if tools is not None:
            tool_kwargs = {
                "tools": tools,
                "tool_choice": tool_choice,
                "parallel_tool_calls": parallel_tool_calls
            }
            client_kwargs.update(tool_kwargs)

        client = OpenAI()

        self.completion = partial(
            client.chat.completions.create,
            temperature=temperature,
            top_p=1.0,
            **client_kwargs
        )

    def generate_response(self, messages, response_format=None):
        try:
            if self.completion:
                # Only pass response_format if it's provided and not None
                kwargs = {}
                if response_format is not None:
                    kwargs["response_format"] = response_format

                response = self.completion(messages=messages, **kwargs)
                return response

            logger.error("Completion function was not properly initialized")
            raise ValueError("Completion function not initialized")

        except Exception as e:
            log_message = exception_log_message(sys.exc_info()[2])
            logger.error(log_message)

            logger.error(f"Exception occurred while generating response: {str(e)}")
            # Re-raise the exception so the calling code can handle it
            raise
