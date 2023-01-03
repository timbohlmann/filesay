import requests
import os
from dotenv import load_dotenv

load_dotenv()
DEV_KEY = os.getenv("DEV_KEY")


def paste(paste_string):
    url = "https://pastebin.com/api/api_post.php"
    values = {
        'api_dev_key': DEV_KEY,
        "api_option": "paste",
        "api_paste_code": paste_string,
        "api_paste_expire_date": "1D"
    }
    response = requests.post(url, values)
    return response.text
