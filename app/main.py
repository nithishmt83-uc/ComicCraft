from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.gemini_flash import generate_outline
from app.gemini_pro import generate_story
from app.image_generator import generate_image
from app.exporters import save_pdf

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

templates = Jinja2Templates(
    directory="app/templates"
)


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.post("/generate")
async def generate(request: Request):

    form = await request.form()

    prompt = form.get("prompt")
    character = form.get("character")
    setting = form.get("setting")
    tone = form.get("tone")
    art_style = form.get("art_style")

    # --------------------------------
    # STEP 1: Generate comic outline
    # --------------------------------

    outline = generate_outline(
        prompt,
        character,
        setting,
        tone,
        art_style
    )

    # --------------------------------
    # STEP 2: Generate complete story
    # --------------------------------

    story = generate_story(outline)

    # --------------------------------
    # STEP 3: Generate ONE large image
    # --------------------------------

    image_paths = []

    story_context = story[:1200]

    image_prompt = f"""
Create ONE large cinematic comic-book illustration
that visually represents the entire story.

Main character: {character}

Setting: {setting}

Tone: {tone}

Art style: {art_style}

The illustration should visually summarize the
important events of the complete comic story.

Create a professional colorful comic-book composition
with the main character clearly visible.

Use expressive characters, dramatic composition,
cinematic lighting, detailed artwork and a polished
AI comic-book appearance.

Keep the character appearance consistent.

Story context:
{story_context}
"""

    try:
        generate_image(
            image_prompt,
            "comic_main.png"
        )

        image_paths.append(
            "/static/images/comic_main.png"
        )

        print("Comic image generated successfully.")

    except Exception as e:
        print(f"Image generation skipped: {e}")

    # --------------------------------
    # STEP 4: Create PDF
    # --------------------------------

    pdf_image_paths = []

    if image_paths:
        pdf_image_paths.append(
            "app/static/images/comic_main.png"
        )

    pdf_path = save_pdf(
        pdf_image_paths,
        story
    )

    # --------------------------------
    # STEP 5: Team Members
    # --------------------------------

    team_members = [
        "👑 Team Leader: Nithish Kumar T",
        "👤 Team Member: Jayakrishna B",
        "👤 Team Member: Harish J",
        "👤 Team Member: Rajesh R",
        "👤 Team Member: Kalaivanan K"
    ]

    # --------------------------------
    # STEP 6: Display Comic Preview
    # --------------------------------

    return templates.TemplateResponse(
        request=request,
        name="comic_preview.html",
        context={
            "outline": outline,
            "story": story,
            "image_paths": image_paths,
            "pdf_url": "/static/images/comiccraft_comic.pdf",
            "team_members": team_members
        }
    )