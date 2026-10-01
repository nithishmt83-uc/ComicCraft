from app.image_generator import generate_image

path = generate_image(
    "A young comic-book hero named Arun holding a mysterious glowing book inside an ancient library, colorful comic book art style, dramatic lighting",
    "test_panel.png"
)

print(path)