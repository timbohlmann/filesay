import requests

def paste(paste_string, dev_key):
    url = "https://pastebin.com/api/api_post.php"
    values = {
        'api_dev_key': dev_key,
        "api_option": "paste",
        "api_paste_code": paste_string,
        "api_paste_expire_date": "1D"
    }
    response = requests.post(url, values)
    return response

