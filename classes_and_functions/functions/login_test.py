import json
def read_data():
    data=None
    with open('static/utils/data.json', 'r') as f:
        data = json.load(f)
    return data

def test_login(email,password):
    data = read_data()
    if(data["email"]==email and data["password"]==password):
        return True
    return False

def update_data(data):
    with open('static/utils/data.json', 'w') as f:
        json.dump(data, f)
    return True