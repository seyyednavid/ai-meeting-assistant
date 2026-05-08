import gradio as gr
from app.pipeline import run_pipeline
import html
import os
import time
from datetime import datetime
import shutil
import uuid



safe_dir = "temp_audio"
os.makedirs(safe_dir, exist_ok=True)


def save_minutes_as_markdown(summary):
    """
    Save generated meeting minutes as a markdown file.
    Returns the file path so Gradio can provide it as a download.
    """
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = os.path.join(output_dir, f"meeting_minutes_{timestamp}.md")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(summary)

    return file_path


def process_audio(file, model_choice, summary_model_choice):
    """
    Process an uploaded audio file and generate meeting minutes.

    This function:
    - Copies the uploaded file to a temporary safe location
    - Runs the transcription and summarization pipeline
    - Formats the transcript for display
    - Saves the generated meeting minutes as a markdown file
    - Returns results and processing details for the UI

    Args:
        file (str): Path to the uploaded audio file from Gradio.
        model_choice (str): Selected transcription model from the UI.
        summary_model_choice (str): Selected summarization model from the UI.

    Returns:
        tuple:
            - transcript_html (str): Formatted transcript for display
            - summary (str): Generated meeting minutes (markdown)
            - markdown_file (str or None): Path to saved markdown file
            - processing_details (str): Information about processing steps
    """
    
    if file is None:
        error_html = """
        <div class="scroll-box transcript-box">
            <pre>Please upload an audio file first.</pre>
        </div>
        """

        processing_details = """
        ### Processing Details
        No audio file uploaded.
        """

        return error_html, "", None, processing_details

    start_time = time.time()
    safe_path = None  

    try:
        # Map UI transcription choice
        if model_choice == "OpenAI GPT-4o Mini Transcribe":
            transcription_model_key = "openai"
        else:
            transcription_model_key = "whisper"

        # Map UI summarization choice
        if summary_model_choice == "OpenAI GPT-4o Mini":
            summarization_model_key = "openai"
        else:
            summarization_model_key = "ollama"

        # 👇 Create safe temp file
        unique_name = f"{uuid.uuid4()}_{os.path.basename(file)}"
        safe_path = os.path.join(safe_dir, unique_name)

        # Copy file safely (handles Windows lock)
        for _ in range(3):
            try:
                shutil.copy(file, safe_path)
                break
            except PermissionError:
                time.sleep(0.5)

        # Run pipeline
        transcript, summary = run_pipeline(
            safe_path,
            transcription_model_key,
            summarization_model_key
        )

        # Processing stats
        processing_time = time.time() - start_time
        transcript_length = len(transcript)

        # Safe HTML display
        safe_transcript = html.escape(transcript)

        transcript_html = f"""
        <div class="scroll-box transcript-box">
            <pre>{safe_transcript}</pre>
        </div>
        """

        # Save markdown
        markdown_file = save_minutes_as_markdown(summary)
        output_filename = os.path.basename(markdown_file)

        processing_details = f"""
        ### Processing Details
        - **Transcription model:** {model_choice}
        - **Summarization model:** {summary_model_choice}
        - **Processing time:** {processing_time:.2f} seconds
        - **Transcript length:** {transcript_length:,} characters
        - **Output file:** {output_filename}
        """

        return transcript_html, summary, markdown_file, processing_details

    except Exception as e:
        safe_error = html.escape(str(e))
        processing_time = time.time() - start_time

        error_html = f"""
        <div class="scroll-box transcript-box">
            <pre>Error: {safe_error}</pre>
        </div>
        """

        processing_details = f"""
        ### Processing Details
        - **Status:** Failed
        - **Transcription model:** {model_choice}
        - **Summarization model:** {summary_model_choice}
        - **Processing time before error:** {processing_time:.2f} seconds
        - **Error:** {safe_error}
        """

        return error_html, "", None, processing_details

    finally:
        # 🧹 Always clean temp file
        if safe_path and os.path.exists(safe_path):
            try:
                os.remove(safe_path)
            except Exception:
                pass


custom_css = """
.main-title {
    text-align: center;
    margin-bottom: 25px;
}

.scroll-box {
    height: 520px;
    overflow-y: auto;
    padding: 18px;
    border: 1px solid #dddddd;
    border-radius: 10px;
    background: #ffffff;
}

.transcript-box pre {
    white-space: pre-wrap;
    word-wrap: break-word;
    font-family: Arial, sans-serif;
    font-size: 13px;
    line-height: 1.5;
}

#generate-btn {
    height: 48px;
    font-size: 16px;
    font-weight: bold;
}

/* Download markdown file */
#download-file {
    min-height: 90px !important;
    max-height: 90px !important;
    overflow: hidden !important;
}

#download-file > div {
    min-height: 90px !important;
    max-height: 90px !important;
    overflow: hidden !important;
}

#download-file .file-preview,
#download-file .file-preview-holder,
#download-file .file-container {
    min-height: 55px !important;
    max-height: 55px !important;
    padding: 6px !important;
    overflow: hidden !important;
}

#download-file svg {
    width: 16px !important;
    height: 16px !important;
}

#download-file .icon-wrap,
#download-file .file-icon {
    width: 18px !important;
    height: 18px !important;
}
"""


with gr.Blocks(
    title="AI Meeting Assistant",
    css=custom_css
) as demo:

    gr.Markdown(
        """
        <div class="main-title">
            <h1>🎤 AI Meeting Assistant</h1>
            <p style="font-size: 16px;">
                Upload a meeting recording and generate structured meeting minutes,
                including key discussion points, decisions, and action items.
            </p>
        </div>
        """
    )

    with gr.Row():

        # Left column: controls
        with gr.Column(scale=1):
            gr.Markdown("### Controls")

            audio_input = gr.Audio(
                sources=["upload"],
                type="filepath",
                label="Upload Meeting Audio",
                elem_id="audio-input"
            )

            model_choice = gr.Dropdown(
                choices=[
                    "OpenAI GPT-4o Mini Transcribe",
                    "HuggingFace Whisper Base"
                ],
                value="OpenAI GPT-4o Mini Transcribe",
                label="Transcription Model"
            )

            summary_model_choice = gr.Dropdown(
                choices=[
                    "OpenAI GPT-4o Mini",
                    "Local qwen-2.5 3B"
                ],
                value="OpenAI GPT-4o Mini",
                label="Summarization Model"
            )

            run_button = gr.Button(
                "Generate Minutes",
                variant="primary",
                elem_id="generate-btn"
            )

            processing_info = gr.Markdown(
                value="",
                label="Processing Details"
            )

            download_file = gr.File(
                label="Download Meeting Minutes (.md)",
                interactive=False,
                elem_id="download-file"
            )

        # Right column: results
        with gr.Column(scale=2):
            gr.Markdown("### Results")

            with gr.Tabs(selected="transcript-tab"):

                with gr.Tab("Transcript", id="transcript-tab"):
                    transcript_output = gr.HTML(
                        label="Transcript"
                    )

                with gr.Tab("Meeting Minutes", id="minutes-tab"):
                    summary_output = gr.Markdown(
                        label="Meeting Minutes",
                        height=520
                    )

    run_button.click(
        fn=process_audio,
        inputs=[
            audio_input,
            model_choice,
            summary_model_choice
        ],
        outputs=[
            transcript_output,
            summary_output,
            download_file,
            processing_info
        ],
        show_progress=True
    )


demo.launch(inbrowser=True)