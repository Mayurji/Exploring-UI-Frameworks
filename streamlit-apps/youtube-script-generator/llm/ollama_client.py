from langchain_community.llms import Ollama

def get_llm(model_name="llama3.2", temperature=0.7):
    return Ollama(
        model=model_name,
        temperature=temperature
    )

