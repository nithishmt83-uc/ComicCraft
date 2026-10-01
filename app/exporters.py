from fpdf import FPDF
from PIL import Image
import os
import re


def clean_text(text):
    text = re.sub(r'[*#`]', '', text)

    text = text.replace("—", "-")
    text = text.replace("–", "-")
    text = text.replace("“", '"')
    text = text.replace("”", '"')
    text = text.replace("’", "'")

    return text.strip()


def save_pdf(image_paths, story, filename="comiccraft_comic.pdf"):

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=12)

    # Find each actual Panel section
    panel_matches = re.findall(
        r'(?is)(?:#+\s*)?\**Panel\s+\d+.*?(?=(?:#+\s*)?\**Panel\s+\d+|$)',
        story
    )

    for i, image_path in enumerate(image_paths):

        pdf.add_page()

        # Panel title
        pdf.set_font("Arial", "B", 16)
        pdf.cell(
            0,
            10,
            f"ComicCraft - Panel {i + 1}",
            ln=True
        )

        # Add image
        if os.path.exists(image_path):

            img = Image.open(image_path)

            width, height = img.size

            max_width = 180
            max_height = 105

            ratio = min(
                max_width / width,
                max_height / height
            )

            display_width = width * ratio
            display_height = height * ratio

            x = (210 - display_width) / 2

            pdf.image(
                image_path,
                x=x,
                y=25,
                w=display_width,
                h=display_height
            )

            pdf.set_y(
                25 + display_height + 8
            )

        # Story heading
        pdf.set_font("Arial", "B", 12)
        pdf.cell(
            0,
            8,
            "Story",
            ln=True
        )

        pdf.set_font("Arial", "", 10)

        # Add the correct panel story
        if i < len(panel_matches):

            panel_text = clean_text(
                panel_matches[i]
            )

            pdf.multi_cell(
                0,
                6,
                panel_text
            )

    # Save PDF
    output_path = os.path.join(
        "app",
        "static",
        "images",
        filename
    )

    pdf.output(output_path)

    return output_path