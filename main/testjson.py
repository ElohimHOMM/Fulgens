import json

with open('main/rules.json') as file:
    payload = json.load(file)
print(payload)
print(type(payload))