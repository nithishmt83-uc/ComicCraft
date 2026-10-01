from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.gemini_flash import generate_outline
from app.gemini_pro import generate_story
from app.image_generator import generate_image
from app.exporters import save_pdf


# ==========================================
# ComicCraft Application
# ==========================================

app = FastAPI()


# ==========================================
# Static files
# ==========================================

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)


# ==========================================
# Templates
# ==========================================

templates = Jinja2Templates(
    directory="app/templates"
)


# ==========================================
# Home Page
# ==========================================

@app.get("/")
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# ==========================================
# Generate Comic
# ==========================================

@app.post("/generate")
async def generate(request: Request):

    # Get form data
    form = await request.form()

    prompt = form.get("prompt")
    character = form.get("character")
    setting = form.get("setting")
    tone = form.get("tone")
    art_style = form.get("art_style")


    # ======================================
    # STEP 1: Generate 5-panel outline
    # ======================================

    outline = generate_outline(
        prompt,
        character,
        setting,
        tone,
        art_style
    )


    # ======================================
    # STEP 2: Generate detailed story
    # ======================================

    story = generate_story(outline)


    # ======================================
    # STEP 3: Generate 5 AI images
    # ======================================

    image_paths = []

    for i in range(1, 6):

        # Keep the prompt within Cloudflare's
        # maximum prompt length
        story_context = story[:1200]

        image_prompt = f"""
Create a colorful comic-book illustration
for panel {i}.

Character: {character}

Setting: {setting}

Tone: {tone}

Art style: {art_style}

Panel number: {i}

Create a scene suitable for this comic.
Keep the main character appearance
consistent across all panels.

Use expressive characters, clear composition,
cinematic lighting, and detailed comic-book
artwork.

Story context:
{story_context}
"""


        # Generate actual AI image
        image_path = generate_image(
            image_prompt,
            f"panel_{i}.png"
        )


        # URL used by the webpage
        image_url = f"/static/images/panel_{i}.png"

        image_paths.append(image_url)


    # ======================================
    # STEP 4: Create PDF
    # ======================================

    pdf_path = save_pdf(
        [
            "app/static/images/panel_1.png",
            "app/static/images/panel_2.png",
            "app/static/images/panel_3.png",
            "app/static/images/panel_4.png",
            "app/static/images/panel_5.png"
        ],
        story
    )


    # ======================================
    # STEP 5: Team Members
    # ======================================

    team_members = [
        "👑 Team Leader: Nithish Kumar T",
        "👤 Team Member: Jayakrishna B",
        "👤 Team Member: Harish J",
        "👤 Team Member: Rajesh R",
        "👤 Team Member: Kalaivanan K"
    ]


    # ======================================
    # STEP 6: Display Comic Preview
    # ======================================

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