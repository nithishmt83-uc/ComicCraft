from app.gemini_flash import generate_outline

result = generate_outline(
    "A young hero discovers a mysterious glowing book.",
    "Arun",
    "An ancient library",
    "Adventure",
    "Colorful comic book"
)

print(result)