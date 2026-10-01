import os
import base64
import requests
from io import BytesIO
from PIL import Image


def generate_image(prompt, filename):

    account_id = os.environ["CLOUDFLARE_ACCOUNT_ID"]
    api_token = os.environ["CLOUDFLARE_API_TOKEN"]

    url = (
        f"https://api.cloudflare.com/client/v4/accounts/"
        f"{account_id}/ai/run/"
        f"@cf/black-forest-labs/flux-1-schnell"
    )

    response = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json",
        },
        json={
            "prompt": prompt
        },
        timeout=180
    )

    if response.status_code != 200:
        raise RuntimeError(
            f"Cloudflare image generation failed: "
            f"{response.status_code} {response.text}"
        )

    data = response.json()

    image_base64 = data["result"]["image"]

    image_bytes = base64.b64decode(image_base64)

    # Open the generated image regardless of
    # the format returned by Cloudflare
    image = Image.open(BytesIO(image_bytes))

    # Convert it to a real PNG
    image = image.convert("RGB")

    output_path = os.path.join(
        "app",
        "static",
        "images",
        filename
    )

    image.save(
        output_path,
        format="PNG"
    )

    return output_path