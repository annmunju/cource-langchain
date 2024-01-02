from langchain import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain

def load_summary_template(summary_path:str) -> str:
    with open(summary_path, 'r') as f:
        summary_raw = f.readlines()
    
    summary_template = '\n'.join([sr.strip() for sr in summary_raw])
    return summary_template


def summary_by_llm_dosent(information):
    summary_template = load_summary_template('src/summary_template.txt')
    summary_prompt_template = PromptTemplate.from_template(summary_template)

    llm = ChatOpenAI(temperature=0)#, model_name="gpt-3.5-turbo")

    chain = LLMChain(llm=llm, prompt=summary_prompt_template)

    result = chain.run(information=information)

    return result

if __name__ == "__main__":
    from third_parties.linkedin import scrape_linkedin_profile
    information = scrape_linkedin_profile()
    print(summary_by_llm_dosent(information))