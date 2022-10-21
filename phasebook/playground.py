from flask import Blueprint, request
from .data.search_data import USERS


bp = Blueprint("users", __name__, url_prefix="/users")

@bp.route("", strict_slashes=False, methods=['GET', 'POST'])
@bp.route("<int:id>",methods=['GET', 'PUT', 'DELETE'])
def search(id = None):
    user_names = [user['name'] for user in USERS]
    user_ids = [int(user['id']) for user in USERS]

    if not id:
        if request.method == 'GET':
            return USERS, 200
        if request.method == 'POST':
            if check_complete_body(request.json):
                return add_user(request.json, user_names, user_ids)
            else:
                return "Invalid JSON", 500
    else:
        
        if id not in user_ids:
                return "Invalid match id", 404
        else:

            index = user_ids.index(id)
            user_data = USERS[index]

            if request.method == 'GET':   
                return user_data, 200

            if request.method == 'PUT':
                return update_user(request.json, index, id, user_names, user_data)

            if request.method == 'DELETE':
                return delete_user(user_data, index)

# Only adds user in runtime
def add_user(req_body, user_names, user_ids):

    if req_body.get('name') in user_names:
        return "Name already exists", 500  
    else:    
        req_body['id'] = str(smallest_available_value(user_ids))

        # USERS[len(USERS)] = req_body
        USERS.append(req_body)

        data = {
            "message" : "New User Added",
            "data" : req_body
        }

        return data, 200



# Only updates user in runtime
def update_user(req_body, index, id, user_names, old_data):
    
    updated_data = {
            "id" : str(id)
    }

    user_names.pop(index)
    
    if req_body.get('name'):
        if req_body.get('name') in user_names:
            return "Name already exists", 500 
        else:
            updated_data['name'] = req_body.get('name')
    else:
        updated_data['name'] = old_data.get('name')
    
    if req_body.get('age'):
        updated_data['age'] = req_body.get('age')
    else:
        updated_data['age'] = old_data.get('age')

    if req_body.get('occupation'):
        updated_data['occupation'] = req_body.get('occupation')
    else:
        updated_data['occupation'] = old_data.get('occupation')

    USERS[index] = updated_data

    user_data = {
        "old" : old_data,
        "updated" : updated_data
    }

    data = {
            "message" : "Existing User Updated",
            "data" : user_data
    }
    return data, 200

# Only deletes user in runtime
def delete_user(user_data, index):

    USERS.pop(index)
    data = {
            "message" : "Existing User Deleted",
            "data" : user_data
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