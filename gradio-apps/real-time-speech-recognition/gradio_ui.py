import gradio as gr
from model import speech_to_text, text_to_speech

# Build the Gradio Interface
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🎙️ Open-Source Audio Toolkit")
    
    with gr.Tab("Speech to Text"):
        with gr.Row():
            audio_input = gr.Audio(sources=["microphone", "upload"], type="filepath", label="Input Audio")
            stt_output = gr.Textbox(label="Transcribed Text", lines=5)
        stt_button = gr.Button("Transcribe")
        stt_button.click(speech_to_text, inputs=audio_input, outputs=stt_output)

    with gr.Tab("Text to Speech"):
        with gr.Row():
            with gr.Column():
                tts_text = gr.Textbox(label="Input Text", placeholder="Type here...", lines=5)
                tts_file = gr.File(label="Or upload a .txt file", file_types=[".txt"])
            tts_audio_output = gr.Audio(label="Generated Audio")
        
        tts_status = gr.Label(label="Status")
        tts_button = gr.Button("Generate Speech")
        tts_button.click(text_to_speech, inputs=[tts_text, tts_file], outputs=[tts_audio_output, tts_status])

demo.launch()