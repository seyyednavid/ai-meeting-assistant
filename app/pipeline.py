from app.transcription import transcribe_openai, transcribe_whisper
from app.summarizer import summarize_openai


def run_pipeline(file_path, transcription_model="openai"):
    # Step 1: Transcription
    if transcription_model == "openai":
        transcript = transcribe_openai(file_path)
    else:
        transcript = transcribe_whisper(file_path)

    # Step 2: Summarization
    summary = summarize_openai(transcript)

    return transcript, summary