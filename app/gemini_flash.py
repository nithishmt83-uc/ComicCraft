from google import genai
import os

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


def generate_outline(prompt, character, setting, tone, art_style):
    instruction = f"""
Create a 5-panel comic story outline.

Story prompt: {prompt}
Character: {character}
Setting: {setting}
Tone: {tone}
Art style: {art_style}

Return exactly 5 panels.
For each panel provide:
1. Panel number
2. Scene description
3. Dialogue

Keep the story connected from panel 1 to panel 5.
"""

    interaction = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=instruction
    )

    return interaction.output_text