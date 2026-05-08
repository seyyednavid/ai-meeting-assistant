from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

OLLAMA_QWEN_MODEL = "qwen2.5:3b"

SYSTEM_PROMPT = """
You are an AI assistant that creates professional meeting minutes from transcripts.

Return the output in clean markdown format without code blocks.

Do not invent information.
If date, location, attendees, owners, or deadlines are not clearly mentioned, write "Not specified" or "Unclear from transcript".

Important rules:
- Decisions are things that were approved, adopted, agreed, moved, seconded, or formally confirmed.
- Action items are follow-up tasks that someone needs to do after the meeting.
- Do not put a decision in the action items table unless there is a clear follow-up task.
- Do not invent owners or deadlines.

Always include these sections:

# Meeting Minutes

## Meeting Overview
- Date:
- Location:
- Attendees:

## Summary
Write a concise summary of the meeting.

## Key Discussion Points
List the main discussion points as bullet points.

## Decisions
List clear decisions or formal meeting outcomes.
If there are no clear decisions, write "No clear decisions identified."

## Action Items
If clear follow-up tasks are found, create a markdown table:
| Task | Owner | Deadline |
|---|---|---|

If no clear follow-up tasks are found, write exactly:
No clear action items identified.

## Takeaways
Write 2-3 short takeaways from the meeting.
"""


def summarize_openai(transcript):
    """
    Generate meeting minutes using OpenAI's GPT model.
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY is missing. Please add it to your .env file.")

    client = OpenAI(api_key=api_key)

    # ✅ limit size BEFORE using it
    transcript = transcript[:20000]

    user_prompt = f"""
Create meeting minutes from the full transcript below.

Important:
- Use the entire transcript, not only the beginning.
- The beginning may include introductory remarks before the formal meeting starts.
- Identify the actual meeting date, location, attendees, decisions, and action items if they appear anywhere in the transcript.
- Do not invent missing information.

Transcript:
{transcript}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0,
        timeout=60
    )

    return response.choices[0].message.content





def summarize_ollama(transcript):
    """
    Generate meeting minutes using a local Qwen model via Ollama.

    The transcript is truncated to reduce processing time and
    avoid context length issues.

    Args:
        transcript (str): Full meeting transcript.

    Returns:
        str: Structured meeting minutes in markdown format.

    Raises:
        RuntimeError: If the Ollama request fails.
    """

    client = OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama"
    )

    transcript_excerpt = transcript[:12000]

    user_prompt = f"""
Create structured meeting minutes from this transcript.

Rules:
- Return only clean markdown
- Do not add explanations
- Do not invent information
- If missing info → write "Not specified"
- If no action items → write exactly: No clear action items identified.

Format:

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

Transcript:
{transcript_excerpt}
"""

    try:
        response = client.chat.completions.create(
            model=OLLAMA_QWEN_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "You generate structured meeting minutes."
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=0,
            max_tokens=800,
            timeout=180
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        raise RuntimeError(f"Ollama summarization failed: {e}")