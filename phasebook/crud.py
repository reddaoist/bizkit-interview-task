from flask import Blueprint, request
from .data.search_data import USERS


bp = Blueprint("users", __name__, url_prefix="/users")

@bp.route("", strict_slashes=False, methods=['GET', 'POST'])
@bp.route("<int:id>",methods=['GET', 'PUT', 'DELETE'])
def search(id = None):
    if not id:
        if request.method == 'GET':
            return USERS, 200
        if request.method == 'POST':
            if check_complete_body(request.json):
                return add_user(request.json)
            else:
                return "Invalid JSON", 500
    else:
        if request.method == 'GET':
            if id < 0 or id > len(USERS):
                return "Invalid match id", 404
            return USERS[id-1], 200
        if request.method == 'PUT':
            if id < 0 or id > len(USERS):
                return "Invalid match id", 404
            return "updates user", 200
        if request.method == 'DELETE':
            if id < 0 or id > len(USERS):
                return "Invalid match id", 404
            return "deletes user", 200

# Only adds user in runtime
def add_user(req_body):
    user_names = [user['name'] for user in USERS]
    user_ids = [int(user['id']) for user in USERS]

    if req_body.get('name') in user_names:
        return "User already exists", 500  
    else:    
        req_body['id'] = str(smallest_available_value(user_ids))

        # USERS[len(USERS)] = req_body
        USERS.append(req_body)

        data = {
            "message" : "New User Added",
            "data" : req_body
        }
        return data, 200


def check_complete_body(jsonData):
    if not jsonData.get('name') or not jsonData.get('age') or not jsonData.get('occupation'):
        return False
    return True

def smallest_available_value(existing_ids):
    new_id = 1
    
    while new_id in existing_ids:
        new_id = new_id + 1
    
    return new_id