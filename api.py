import io
import cv2
import requests
from PIL import Image
from requests_toolbelt.multipart.encoder import MultipartEncoder


def detect_api(path):
    # Load Image with PIL
    img = cv2.imread(path)
    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pilImage = Image.fromarray(image)

    # Convert to JPEG Buffer
    buffered = io.BytesIO()
    pilImage.save(buffered, quality=100, format="JPEG")

    # Build multipart form and post request
    m = MultipartEncoder(fields={'file': ("imageToUpload", buffered.getvalue(), "image/jpeg")})

    response = requests.post("https://detect.roboflow.com/slide_captcha/4?api_key=FfxewQzijAWou4AD7Rem", data=m,
                             headers={'Content-Type': m.content_type})

    # print(response)
    # print(response.json())
    return response.json()

path = "data/images/img.png"
info = detect_api(path)
predictions = info['predictions']
print(predictions[0])
print(predictions[0]['x'])
