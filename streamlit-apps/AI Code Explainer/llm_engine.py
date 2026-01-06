import ollama
from prompts import *

def explain_code(code_snippet, model_name="llama3.2"):
    """
    Sends code to the local Ollama instance and returns an explanation.
    """
    system_prompt = (SYSTEM_PROMPT)
    
    response = ollama.chat(
        model=model_name,
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': f"Explain this code:\n\n{code_snippet}"},
        ],
        stream=True # Enabling streaming for a better UI experience
    )

    return response