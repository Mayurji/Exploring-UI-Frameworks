import gradio as gr
from config.models import SUPPORTED_MODELS, VISION_MODELS
from core.ollama_client import stream_chat
from core.storage import save_chat, load_chat

def toggle_image(model):
    return gr.update(visible=model in VISION_MODELS)

def chat_fn(model, message, image, history, temperature, top_p):
    history = history or []

    response_stream = stream_chat(
        model,
        message,
        image,
        history,
        temperature,
        top_p
    )

    assistant_reply = ""
    for partial in response_stream:
        assistant_reply = partial
        yield history + [(message, assistant_reply)]

    history.append((message, assistant_reply))
    save_chat(history)
