# Audio Chatbot Application

This project implements an audio-based chatbot that allows users to interact with a language model via speech. The application uses Whisper for speech-to-text, a ChatModel for generating responses, and TTS for converting text responses back to speech.

## Features

- Converts speech to text using Whisper.
- Generates conversational responses using a ChatModel.
- Converts text responses to speech using TTS.
- Provides a web interface for recording and submitting audio inputs.

## Requirements

- Python 3.10+
- Flask
- [whisper](https://github.com/openai/whisper.git)
- torch
- [llamafactory](https://github.com/hiyouga/LLaMA-Factory.git)
- [TTS](https://github.com/coqui-ai/TTS.git)
- gradio
- requests

## Installation

1. Clone the repository:

```sh
git clone https://github.com/yourusername/audio-chatbot.git
cd audio-chatbot
```

2. Install the required Python packages:

```sh
pip install -r requirements.txt
```

3. Prepare the necessary model files:
   - Whisper model
   - [TTS model](https://github.com/coqui-ai/TTS/releases/tag/v0.6.1_models)
   - Large language model (e.g., "[meta-llama/Meta-Llama-3-8b](https://huggingface.co/meta-llama/Meta-Llama-3-8B)" from Huggingface)

4. Update the `backend.py` file with the paths to your models if needed.

## Usage

### Backend

1. Start the Flask server:

```sh
python backend.py
```

The server will start running on `http://0.0.0.0:6006`.

### Frontend

1. Start the Gradio interface:

```sh
python app.py
```

The Gradio interface will launch and provide a URL for accessing the web interface.

## API Endpoints

### `POST /process_audio`

This endpoint accepts an audio file, processes it to generate a response, and returns the response as an audio file.

#### Request

- `audio`: The audio file to be processed.

#### Response

- An audio file containing the generated response.

### `POST /clear_history`

This endpoint clears the conversation history.

#### Response

- JSON message confirming the history has been removed.

## Example

1. Open the provided URL from the Gradio interface.
2. Record your answer using the "Record Your Answer" button.
3. Click the "Submit" button to send the audio to the backend.
4. The response will be generated and played back as an audio file.

## Contributing

If you would like to contribute to this project, please open an issue or submit a pull request on GitHub.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [Whisper](https://github.com/openai/whisper) for speech-to-text conversion.
- [llamafactory](https://github.com/llamafactory/llama3) for the ChatModel.
- [TTS](https://github.com/coqui-ai/TTS) for text-to-speech synthesis.
- [Gradio](https://github.com/gradio-app/gradio) for the user interface.
