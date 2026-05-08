from transformers import pipeline
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

# Lazy load whisper
whisper_pipe = None


def transcribe_openai(file_path):
    """
    Transcribe an audio file using OpenAI's transcription API.

    Args:
        file_path (str): Path to the audio file.

    Returns:
        str: Transcribed text.
    """
    
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY is missing. Please add it to your .env file.")

    client = OpenAI(api_key=api_key)
    
    with open(file_path, "rb") as f:
        result =  client.audio.transcriptions.create(
            model="gpt-4o-mini-transcribe",
            file=f
        )
        
    return result.text




def transcribe_whisper(file_path):
    """
    Transcribe an audio file using a local Whisper model.

    The model is loaded only once (lazy loading) and reused
    for subsequent calls to improve performance.

    Args:
        file_path (str): Path to the audio file.

    Returns:
        str: Transcribed text.
    """
    global whisper_pipe
    
    if whisper_pipe is None:
        whisper_pipe = pipeline(
            "automatic-speech-recognition",
            model = "openai/whisper-base",
            return_timestamps=True,
            chunk_length_s=30,
            stride_length_s=5
        )
    
    result = whisper_pipe(file_path)
    return result["text"]
    


