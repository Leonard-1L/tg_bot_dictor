import logging

import requests


def make_requests(user_text: str):
    headers = {
        'Authorisation': "t1.9eumcmWi5GYz5CTkJPJkZrl3z9zESHU_573NANgz-zef1656VmpiQz4qNmJiVnpzPjpeckpGc7_zF656VmpiQz4qNmJiVnpzPjpeckpGcveuelZqSmJKMjp6JzY2Uj4qQm4zPyLXehpzRnJCSj4qLmtGLmdKckJKPioua0pKai56bnoue0oye.DzU2CWUlWrf9QmTXU4IN5t1af7zy-T2GTvHTkgvG45enUU4WPYyCpK3OAiTeerhk4CCnKjwc9joVMNCRszzsBA"
    }
    data = {
        "text": user_text,
        'lang': 'ru=RU',
        'voice': 'zahar',
        'folderId': "b1gpkb6hb5db01d7ohct"
    }
    response = requests.post('https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize', headers=headers, data=data)
    if response.status_code == 200:
        return response.content
    else:
        logging.error(f"о НЬЕТ!1! КАКАЯТО хЕРНЯ СЛУЧТЛАСЬ:{response.status_code}")

