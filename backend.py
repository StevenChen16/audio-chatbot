from flask import Flask, request, jsonify, send_file
import whisper
import torch
from llamafactory.chat import ChatModel
from llamafactory.extras.misc import torch_gc
from TTS.api import TTS

app = Flask(__name__)

# 初始化 Whisper 模型
whisper_model = whisper.load_model("/root/base.pt")

# 初始化对话生成模型
chat_model_args = dict(
  model_name_or_path="/root/autodl-tmp/llama3-model", # use bnb-4bit-quantized Llama-3-8B-Instruct model
  template="llama3",                     # same to the one in training
  finetuning_type="lora",                  # same to the one in training
  quantization_bit=8,                    # load 4-bit quantized model
  use_unsloth=True,                     # use UnslothAI's LoRA optimization for 2x faster generation
)
chat_model = ChatModel(chat_model_args)

# 初始化 TTS 模型
# tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)
tts = TTS(model_name="tts_models/en/ljspeech/vits", progress_bar=False)
device = "cuda" if torch.cuda.is_available() else "cpu"
tts = tts.to(device)

conversation_history = []

background_prompt = """
"""

@app.route('/process_audio', methods=['POST'])
def process_audio():
    print("received user's answer. Processing.")
    
    audio_file = request.files['audio']
    audio_path = "temp_audio.m4a"
    audio_file.save(audio_path)

    # 使用 Whisper 将音频转换为文字
    audio = whisper.load_audio(audio_path)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(whisper_model.device)
    options = whisper.DecodingOptions()
    result = whisper.decode(whisper_model, mel, options)
    text = result.text
    print("User answer: {}".format(text))

    # 将用户输入添加到对话历史记录中
    conversation_history.append({"role": "user", "content": background_prompt+text})

    # 使用对话生成模型生成回答
    response = ""
    for new_text in chat_model.stream_chat(conversation_history):
        response += new_text

    # 将模型生成的回答添加到对话历史记录中
    conversation_history.append({"role": "assistant", "content": response})

    # 使用 TTS 生成语音
    output_audio_path = "output_audio.wav"
    tts.tts_to_file(response, file_path=output_audio_path, speed_factor=1.5)

    return send_file(output_audio_path, mimetype="audio/wav")

@app.route('/clear_history', methods=['POST'])
def clear_history():
    global conversation_history
    conversation_history = []
    torch_gc()
    return jsonify({"message": "History has been removed."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6006)