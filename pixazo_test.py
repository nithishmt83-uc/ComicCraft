import os
import requests

url = "https://gateway.pixazo.ai/flux-1-schnell/v1/getDataBatch"

headers = {
    "Content-Type": "application/json",
    "Cache-Control": "no-cache",
    "Ocp-Apim-Subscription-Key": os.environ["PIXAZO_API_KEY"]
}

data = {
    "prompt": "A colorful comic book illustration of a young superhero standing on a futuristic city street, dramatic lighting, detailed comic art",
    "num_steps": 4,
    "seed": 15,
    "height": 512,
    "width": 512
}

response = requests.post(url, json=data, headers=headers)

print("STATUS:", response.status_code)
print("RESPONSE:", response.text)