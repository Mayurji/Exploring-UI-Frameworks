from langchain_classic.chains.llm import LLMChain
from llm.ollama_client import get_llm
from prompts.prompts import HOOK_PROMPT, SCRIPT_PROMPT, TITLE_PROMPT

def generate_script(topic, tone, duration, model_name='llama3.2'):
    llm = get_llm(model_name=model_name)
    chain = LLMChain(llm=llm, prompt=SCRIPT_PROMPT)

    return chain.run(
        topic=topic,
        tone=tone,
        duration=duration
    )

def generate_titles(topic, model_name='llama3.2'):
    llm = get_llm(model_name=model_name, temperature=0.9)
    chain = LLMChain(llm=llm, prompt=TITLE_PROMPT)
    return chain.run(topic=topic)

def generate_hooks(topic, model_name='llama3.2'):
    llm = get_llm(model_name=model_name, temperature=0.9)
    chain = LLMChain(llm=llm, prompt=HOOK_PROMPT)
    return chain.run(topic=topic)
