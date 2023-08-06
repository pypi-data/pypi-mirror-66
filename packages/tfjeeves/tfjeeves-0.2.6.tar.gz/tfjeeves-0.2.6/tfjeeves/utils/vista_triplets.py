import json

import jwt
import pytz
import requests
import base64
from pathlib import Path
from datetime import datetime
from urllib.request import urlopen
from PIL import Image


def run(img_path: str, model_slug: str, dst: str, num_result: int):
    img_path = Path(img_path)
    dst = Path(dst)
    dst.mkdir(exist_ok=True, parents=True)
    tz = pytz.timezone("Asia/Kolkata")
    t = datetime.now(tz).timestamp()
    payload = {
        "agent": f"save-result",
        "userid": "123456",
        "t": t
    }
    auth_token = jwt.encode(payload, "live-FQpQfuJxTBCR9f7c", 'HS256')
    headers = {'authorization': 'Bearer ' + auth_token.decode('utf-8'), 'Content-Type': "application/json"}

    image_binary = base64.b64encode(img_path.open("rb").read())
    request_payload = json.dumps({
        "t_sent": t,
        "model": model_slug,
        "attach_images": "yes",
        "image": str(image_binary.decode('utf-8'))
    })

    response = requests.post(url="https://canary-vista-api-shop101.fp0.in/v1/similar-catalogues", headers=headers, data=request_payload)
    results = json.loads(response.text)["catalogues"]
    for i, result in enumerate(results):
        img = Image.open(urlopen(result["image_url"]))
        img.save(dst / f"{img_path.stem}_{model_slug}_{i}.jpeg")
        if i == num_result - 1:
            break
