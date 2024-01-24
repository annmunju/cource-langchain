from dotenv import load_dotenv
from langchain.tools import tool, render
from langchain import hub
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI

obj = hub.pull("hwchase17/react")

load_dotenv("../../.env")


@tool
def get_text_length(text: str) -> int:
    """Returns the length of a text by characters"""
    return len(text)


if __name__ == "__main__":
    tools = [get_text_length]
    template = obj.template.replace("{agent_scratchpad}", "")
    prompt = PromptTemplate.from_template(template=template).partial(
        tools=render.render_text_description(tools), tool_names=", ".join([t.name for t in tools])
    )

    llm = ChatOpenAI(temperature=0, stop=["\nObservation"])

