import json
import os

path: str = 'main/data/'

def get_payload(file_name) -> str:
    with open(path + file_name + '.json') as file:
        payload: dict = json.load(file)
    return payload

def save_payload(file_name, payload):
    with open(path + file_name + '.json', 'w') as file:
        json.dump(payload, file, ensure_ascii=False, indent=4)

def backup_json(file_name: str):
    if not os.path.exists(path + file_name + '.json'):
        print(f'ERROR: File to Backup does not exist')
        return 'ERROR'
    payload = get_payload(file_name)
    create_file(path + file_name + '_backup.json')
    save_payload(file_name + '_backup', payload)

def create_file(file_name):
    file = open(file_name, 'w')
    file.write('')
    file.close()