import whisper
from gtts import gTTS

# Load the Whisper model (Small is a good balance of speed and accuracy)
stt_model = whisper.load_model("base")

def speech_to_text(audio):
    if audio is None:
        return "Please upload or record audio."
    # Transcribe the audio file
    result = stt_model.transcribe(audio)
    return result["text"]

def text_to_speech(text, file):
    # Determine input source: text box or uploaded file
    input_text = ""
    if file is not None:
        with open(file.name, "r", encoding="utf-8") as f:
            input_text = f.read()
    elif text:
        input_text = text
    
    if not input_text.strip():
        return None, "No text provided."

    # Generate speech
    tts = gTTS(input_text)
    output_path = "output.mp3"
    tts.save(output_path)
    return output_path, "Conversion successful!"