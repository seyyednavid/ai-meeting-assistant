from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

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
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY is missing. Please add it to your .env file.")

    client = OpenAI(api_key=api_key)

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
        temperature=0
    )

    return response.choices[0].message.content