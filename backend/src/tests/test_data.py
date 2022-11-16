import json

def get_user(role):
    with open('test_data.json', 'r') as file:
        data = file.read().replace('\n', '')

    users = json.loads(data)['test_users']
    for user in users:
        if user['role'] == role:
            return user

print(get_user('member'))