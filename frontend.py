import gradio as gr
import requests
import os

def process_audio(audio):
    if audio is None:
        return None
    files = {'audio': (os.path.basename(audio), open(audio, 'rb'), 'audio/wav')}
    response = requests.post('http://localhost:6006/process_audio', files=files)
    response_audio_path = 'response_audio.wav'
    with open(response_audio_path, 'wb') as f:
        f.write(response.content)
    return response_audio_path

def record_and_process(audio):
    return process_audio(audio)

with gr.Blocks() as demo:
    audio_input = gr.Audio(type="filepath", label="Record Your Answer",)
    output_audio = gr.Audio(label="Response")
    submit_button = gr.Button("Submit")

    submit_button.click(record_and_process, inputs=audio_input, outputs=output_audio).then(
        lambda: gr.update(interactive=True), None, [submit_button]
    )
    
    demo.launch(share=True)