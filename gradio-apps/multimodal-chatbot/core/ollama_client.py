import ollama
from config.models import VISION_MODELS
from core.image_utils import image_to_base64

def stream_chat(model, message, image, history, temperature, top_p):
    messages = []

    for user, assistant in history:
        messages.append({"role": "user", "content": user})
        messages.append({"role": "assistant", "content": assistant})

    payload = {"role": "user", "content": message}

    if image and model in VISION_MODELS:
        payload["images"] = [image_to_base64(image)]

    messages.append(payload)

    stream = ollama.chat(
        model=model,
        messages=messages,
        stream=True,
        options={
            "temperature": temperature,
            "top_p": top_p
        }
    )

    full_response = ""
    for chunk in stream:
        token = chunk["message"]["content"]
        full_response += token
        yield full_response
