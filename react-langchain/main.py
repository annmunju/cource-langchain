from dotenv import load_dotenv
from typing import Union, List
from langchain.tools import tool, render, Tool
from langchain import hub
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.agents.output_parsers.react_single_input import ReActSingleInputOutputParser
from langchain_core.agents import AgentAction, AgentFinish


obj = hub.pull("hwchase17/react")

load_dotenv("../../.env")


@tool
def get_text_length(text: str) -> int:
    """Returns the length of a text by characters"""
    return len(text)

def find_tool_by_name(tools: List[Tool], tool_name:str) -> Tool:
    for tool in tools:
        if tool.name == tool_name:
            return tool
    raise ValueError(f"Tool with name {tool_name}.")

if __name__ == "__main__":
    tools = [get_text_length]
    template = obj.template.replace("{agent_scratchpad}", "")
    prompt = PromptTemplate.from_template(template=template).partial(
        tools=render.render_text_description(tools), tool_names=", ".join([t.name for t in tools])
    )

    llm = ChatOpenAI(temperature=0, model_kwargs={"stop": ["\nObservation"]})
    agent = {"input": lambda x: x["input"]} | prompt | llm | ReActSingleInputOutputParser() # LCEL 
    
    agent_step: Union[AgentAction, AgentFinish] = agent.invoke({"input" : "What is the length in characters of the text DOG?"})
    
    if isinstance(agent_step, AgentAction):
        tool_name = agent_step.tool
        tool_to_use = find_tool_by_name(tools, tool_name)
        tool_input = agent_step.tool_input
        
        observation = tool_to_use.func(str(tool_input))
        print(f"{observation=}")
    # print(agent_step) # tool='get_text_length' tool_input="'DOG'" log="Since we have the tool get_text_length, we can use it to find the length of the text 'DOG'.\nAction: get_text_length\nAction Input: 'DOG'"
