from google import genai
import os

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


def generate_story(outline):
    instruction = f"""
Turn the following 5-panel comic outline into a detailed comic story.

5-panel outline:
{outline}

For each of the 5 panels, provide:
1. Panel number
2. Narration
3. Character dialogue
4. Important visual details for the illustration

Keep the characters, story, setting, and events consistent across all panels.
Make the dialogue natural and suitable for a comic.
"""

    interaction = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=instruction
    )

    return interaction.output_text