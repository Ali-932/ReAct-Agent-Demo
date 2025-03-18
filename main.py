import json
import sys

from dotenv import load_dotenv

from agents.react_agent import ReactAgent
from clients.open_ai_client import OpenAIClient
from config.chat_examples import EXAMPLES
from utils.helper_functions import get_args
from config.system_prompt import REACT_SYSTEM_PROMPT_TEMPLATE
from utils.error_handler import exception_log_message
from utils.logger import setup_logger
from tools.tool_setup import get_tools, create_sys_prompt

# Create a logger specific to this module
logger = setup_logger('main')


def run(args):
    tools = get_tools()

    tool_calls = [tool.tool_call for name, tool in tools.items()]
    client = OpenAIClient(
        args.model,
        num_requests=1,
        temperature=args.temperature,
        tools=tool_calls,
        tool_choice="auto",
    )

    sys_prompt = create_sys_prompt(tools, REACT_SYSTEM_PROMPT_TEMPLATE, EXAMPLES, logger)

    with open("config/user_prompts.json", "r") as file:
        input_json = json.load(file)

    agent = ReactAgent(
        client,
        sys_prompt,
        num_steps=args.num_steps,
        tools=tools
    )

    for user_request in input_json["user_requests"]:

        try:

            result = agent.generate_response(user_request)
            if result:
                logger.info(f"Final answer : {result}")

        except Exception as e:
            print(sys.exc_info())
            log_message = exception_log_message(sys.exc_info()[2])
            logger.error(log_message)
            logger.error(f"The following error occurred while processing the user request : {user_request}")
            logger.error(f"\n{e}")


if __name__ == "__main__":
    load_dotenv()
    args = get_args()
    run(args)
