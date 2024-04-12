import logging
import requests
from config import iam_token, folder_id
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="logs.txt",
    filemode="w"
)


def make_requests(user_text: str):
    headers = {
        'Authorization': f'Bearer {iam_token}'
    }
    data = {
        "text": user_text,
        'lang': 'ru=RU',
        'voice': 'zahar',
        'folderId': folder_id
    }
    response = requests.post('https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize', headers=headers, data=data)
    if response.status_code == 200:
        return True, response.content
    else:
        logging.error(f"0 НЬЕТ!1! КАКАЯТО ФИНГНГЯ СЛУЧТЛАСЬ. КОД ОШИБКИ:{response.status_code}")
        return False, f"При запросе произошла непредвиденная ошибка. Статус ошибки: {response.status_code}"
