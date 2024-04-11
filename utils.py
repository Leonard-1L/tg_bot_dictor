import json

users_file = "users_data.json"


def load_users_data():
    try:
        with open(users_file, "r", encoding="utf-8") as file:
            users_data = json.load(file)
            return users_data
    except json.decoder.JSONDecodeError:
        return {}
    except FileNotFoundError:
        with open(users_file, 'w') as json_file:
            return json_file.write("{}")


def save_users_data(data):
    with open(users_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=3, ensure_ascii=False)
