import gradio as gr
from ui.layout import chat_fn, toggle_image
from config.models import SUPPORTED_MODELS
from core.storage import load_chat

# Custom CSS for black borders
css = """
.gradio-container {
    --border-color-primary: black !important;
    --border-color-accent: black !important;
}
"""

with gr.Blocks(title="Ollama Multimodal Chat", css=css) as demo:
    with gr.Sidebar():
        gr.Markdown("### ⚙️ Settings")
        model = gr.Dropdown(
            SUPPORTED_MODELS,
            value="llava:latest",
            label="Model"
        )
        temperature = gr.Slider(0.0, 1.5, value=0.7, label="Temperature")
        top_p = gr.Slider(0.1, 1.0, value=0.9, label="Top-P")
        
        gr.Markdown("---")
        send = gr.Button("Send 🚀", variant="primary")

    with gr.Column():
        gr.Markdown("## 🧠 Ollama Multimodal Chatbot")
        
        chatbot = gr.Chatbot(
            value=load_chat(),
            height=600
        )

        with gr.Row():
            message = gr.Textbox(
                label="Message",
                placeholder="Ask something…",
                lines=3,
                scale=1
            )
            image = gr.Image(
                type="pil",
                label="Image",
                visible=True,
                scale=1
            )

    model.change(toggle_image, model, image)

    send.click(
        chat_fn,
        inputs=[model, message, image, chatbot, temperature, top_p],
        outputs=chatbot
    )

if __name__ == "__main__":
    demo.launch()
