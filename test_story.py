from app.gemini_flash import generate_outline
from app.gemini_pro import generate_story

outline = generate_outline(
    "A young hero discovers a mysterious glowing book.",
    "Arun",
    "An ancient library",
    "Adventure",
    "Colorful comic book"
)

story = generate_story(outline)

print(story)