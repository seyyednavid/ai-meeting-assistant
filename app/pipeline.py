from app.transcription import transcribe_openai, transcribe_whisper
from app.summarizer import summarize_openai, summarize_ollama
import logging


def run_pipeline(file_path, transcription_model="openai", summarization_model="openai"):
    """
    Run the full AI pipeline: transcription followed by summarization.

    Args:
        file_path (str): Path to the audio file.
        transcription_model (str): Model to use for transcription ("openai" or "whisper").
        summarization_model (str): Model to use for summarization ("openai" or "ollama").

    Returns:
        tuple: (transcript, summary)
            transcript (str): Transcribed text from audio
            summary (str): Generated meeting minutes in markdown format
    """
    # Step 1: Transcription
    if transcription_model == "openai":
        transcript = transcribe_openai(file_path)
    else:
        transcript = transcribe_whisper(file_path)
        
    # Step 2: Summarization (uses fallback to OpenAI if Ollama fails)
    try:
        if summarization_model == "openai":
            summary = summarize_openai(transcript)
        else:
            summary = summarize_ollama(transcript)

    except Exception as e:
        logging.warning("Ollama failed, fallback to OpenAI: %s", e)
        summary = summarize_openai(transcript)

    return transcript, summary