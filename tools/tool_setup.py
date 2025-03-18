from utils.helper_functions import get_method_list
from tools import Tool, tool_methods


def get_tools():
    function_list = get_method_list(tool_methods)
    tools = {}
    for func in function_list:
        tools[func.__name__] = Tool(func)

    return tools


def create_tool_description(tools):
    tool_description = ""

    for i, (name, tool) in enumerate(tools.items()):
        tool_description += f"{str(i + 1)}. **{tool.name}**: {tool.description} \n"

    return tool_description


def create_sys_prompt(tools, prompt_template, examples, logger):
    tool_description = create_tool_description(tools)

    sys_prompt = prompt_template.format(examples=examples, external_tools=tool_description)

    logger.info(f" System prompt:\n + {sys_prompt}")

    return sys_prompt
