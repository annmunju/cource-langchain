from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from output_parsers import PersonIntel, person_intel_parser

from typing import Tuple


def load_summary_template(summary_path: str) -> str:
    with open(summary_path, "r") as f:
        summary_raw = f.readlines()

    summary_template = "\n".join([sr.strip() for sr in summary_raw])
    return summary_template


def summary_ice_breaker(name: str) -> Tuple[PersonIntel, str]:
    linkedin_profile_url = linkedin_lookup_agent(
        name=name  # "Eden Marco"
    )  # 이름에 힌트를 추가하면 조금 더 잘나온다~
    information = scrape_linkedin_profile(linkedin_profile_url)

    summary_template = load_summary_template("src/summary_template.txt")
    summary_prompt_template = PromptTemplate(
        input_variables=["information"],
        template=summary_template,
        partial_varibles=["format_instructions"],
    )

    llm = ChatOpenAI(temperature=0)  # , model_name="gpt-3.5-turbo")

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    result = chain.run(
        information=information,
        format_instructions=person_intel_parser.get_format_instructions(),
    )

    return person_intel_parser.parse(result), information.get("profile").get(
        "profile_pic_url"
    )


if __name__ == "__main__":
    print(summary_ice_breaker(name="Eden Marco"))
