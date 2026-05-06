# 🎤 AI Meeting Assistant

AI Meeting Assistant is an end-to-end AI application that converts meeting audio into structured meeting minutes.
The app supports audio transcription, meeting summarization, action-item extraction, transcript viewing, processing details, and Markdown export.

This project was built as a practical AI Engineering portfolio project to demonstrate the design of a modular AI pipeline using both closed-source and open-source model options.

---
## 📸 Screenshots

### Application UI
![Application UI](images/app-ui.jpg)

---

## 🚀 Features

- Upload meeting audio files
- Transcribe audio using:
  - OpenAI transcription API
  - HuggingFace Whisper
- Generate structured meeting minutes using OpenAI GPT
- View the full transcript
- View professional meeting minutes
- Extract:
  - Meeting overview
  - Summary
  - Key discussion points
  - Decisions
  - Action items
  - Takeaways
- Download generated meeting minutes as a Markdown file
- Display processing details:
  - transcription model used
  - summarization model used
  - processing time
  - transcript length
  - output filename
- Interactive Gradio user interface

---

## 🧠 Project Goal

The goal of this project is to build a practical AI assistant that can help users convert meeting recordings into useful written documentation.

The project demonstrates:

- speech-to-text processing
- large language model summarization
- prompt engineering
- modular AI pipeline design
- open-source vs closed-source model trade-offs
- user-facing AI application development
- Markdown output generation

---

## 🏗️ Architecture

```text
Audio Upload
    ↓
Transcription
    ├── OpenAI Transcription
    └── HuggingFace Whisper
    ↓
Transcript
    ↓
Meeting Minutes Generation
    └── OpenAI GPT
    ↓
Results
    ├── Transcript tab
    ├── Meeting Minutes tab
    ├── Processing Details
    └── Markdown Download
```

---

## 📁 Project Structure

```text
ai-meeting-assistant/
│
├── app/
│   ├── __init__.py
│   ├── pipeline.py
│   ├── transcription.py
│   └── summarizer.py
│
├── ui/
│   ├── __init__.py
│   └── gradio_app.py
│
├── outputs/
│   └── generated meeting minutes files
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🧩 Main Components

### 1. Transcription Module

Located in:

```text
app/transcription.py
```

This module handles audio-to-text conversion.

It currently supports:

#### OpenAI Transcription

Uses:

```text
gpt-4o-mini-transcribe
```

This option is fast and suitable for longer audio files.

#### HuggingFace Whisper

Uses:

```text
openai/whisper-base
```

This provides a free/open-source transcription option.

Note: HuggingFace Whisper runs locally and can be slow on CPU for long audio files.

---

### 2. Summarization Module

Located in:

```text
app/summarizer.py
```

This module converts transcripts into structured meeting minutes using OpenAI GPT.

The generated output includes:

- Meeting overview
- Summary
- Key discussion points
- Decisions
- Action items
- Takeaways

The summarization model is currently:

```text
gpt-4o-mini
```

---

### 3. Pipeline Module

Located in:

```text
app/pipeline.py
```

This module connects transcription and summarization into one workflow:

```text
Audio file → Transcript → Meeting minutes
```

---

### 4. Gradio UI

Located in:

```text
ui/gradio_app.py
```

The Gradio interface allows users to:

- upload audio
- choose the transcription model
- generate meeting minutes
- view transcript
- view meeting minutes
- download Markdown output
- check processing details

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/ai-meeting-assistant.git
cd ai-meeting-assistant
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

#### Windows PowerShell

```bash
.venv\Scripts\Activate
```

#### macOS/Linux

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

You can also create a `.env.example` file:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

Do not commit your real `.env` file to GitHub.

---

## 🎵 FFmpeg Requirement

HuggingFace Whisper requires FFmpeg to process audio files.

### Windows

Install with:

```bash
winget install Gyan.FFmpeg
```

Then restart your terminal or VS Code and check:

```bash
ffmpeg -version
```

### macOS

```bash
brew install ffmpeg
```

### Linux

```bash
sudo apt update
sudo apt install ffmpeg
```

---

## ▶️ Running the App

Run the Gradio app from the project root:

```bash
python -m ui.gradio_app
```

Then open the local URL shown in the terminal, usually:

```text
http://127.0.0.1:7860
```

---

## 🧪 How to Use

1. Upload a meeting audio file.
2. Choose a transcription model:
   - OpenAI Transcription
   - HuggingFace Whisper
3. Click **Generate Minutes**.
4. View the transcript in the **Transcript** tab.
5. View generated meeting minutes in the **Meeting Minutes** tab.
6. Download the meeting minutes as a `.md` file.
7. Review processing details in the left panel.

---

## 📊 Model Options and Trade-offs

| Component | Model | Type | Notes |
|---|---|---|---|
| Transcription | OpenAI `gpt-4o-mini-transcribe` | Closed-source API | Fast and reliable |
| Transcription | HuggingFace `openai/whisper-base` | Open-source/local | Free but slower on CPU |
| Summarization | OpenAI `gpt-4o-mini` | Closed-source API | Produces structured and high-quality meeting minutes |

---

## ⚠️ Current Limitations

- HuggingFace Whisper can be slow for long audio files when running on CPU.
- Speaker diarization is not included in Version 1.
- The summarization model is currently OpenAI only.
- Very long transcripts may require chunking in future versions.
- Attendee names may be affected by transcription accuracy.

---

## 🔮 Future Improvements

Planned improvements include:

- Add open-source summarization model
- Add transcript caching to avoid re-processing the same audio file
- Add speaker diarization
- Export to PDF
- Add Docker support
- Add cloud deployment
- Add better support for long meetings through transcript chunking
- Add model comparison dashboard for speed, cost, and quality

---

## 🧠 What I Learned

This project helped me practise:

- building modular AI applications
- integrating speech-to-text models
- using OpenAI APIs
- using HuggingFace pipelines
- designing prompt templates for structured outputs
- handling environment variables
- building an interactive Gradio interface
- tracking processing metadata
- exporting generated content

---

## 📌 Example Output

The app generates meeting minutes in this format:

```markdown
# Meeting Minutes

## Meeting Overview
- Date:
- Location:
- Attendees:

## Summary

## Key Discussion Points

## Decisions

## Action Items

## Takeaways
```

---

## 🛠️ Technologies Used

- Python
- Gradio
- OpenAI API
- HuggingFace Transformers
- Whisper
- PyTorch
- FFmpeg
- python-dotenv

---

## 📄 License

This project is intended for learning and portfolio purposes.

---

## 👤 Author

Developed by Seyyednavid Hejazijouybari as an AI Engineering portfolio project.
