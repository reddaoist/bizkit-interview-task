from flask import Blueprint, request, jsonify
from ...models import User, db, Interest


bp = Blueprint("usersv2", __name__, url_prefix="/v2/users")

@bp.route("", strict_slashes=False, methods=['GET', 'POST'])
@bp.route("<int:id>",methods=['GET', 'PUT', 'DELETE'])
def search(id = None):

    users = jsonify(User.query.all())

    user_names = [user['name'].lower() for user in users.json]
    user_ids = [int(user['id']) for user in users.json]

    if not id:
        if request.method == 'GET':
            return users
        if request.method == 'POST':
            if check_complete_body(request.json):
                return add_user(request.json, user_names)
            else:
                return "Invalid JSON", 500
    else:
        
        if id not in user_ids:
                return "Invalid id", 404
        else:

            user_data = jsonify(User.query.filter_by(id=id).first())

            if request.method == 'GET':   
                return user_data

            if request.method == 'PUT':
                return update_user(request.json, id, user_names, user_data.json)

            if request.method == 'DELETE':
                return delete_user(user_data.json, id)

# Only adds user in runtime
def add_user(req_body, user_names):

    if req_body.get('name').lower() in user_names:
        return "Name already exists", 500  
    else:    
        query = User(name=req_body.get('name'), age=req_body.get('age'), occupation=req_body.get('occupation'))
        db.session.add(query)
        db.session.commit()

        new_user = jsonify(User.query.filter_by(name=req_body.get('name')).first())

        data = {
            "message" : "New User Added",
            "data" : new_user.json
        }

        return data, 200



# Only updates user in runtime
def update_user(req_body, id, user_names, old_data):
    
    user_data = User.query.filter_by(id=id).first()

    updated_data = {
            "id" : old_data.get('id')
    }
    
    if req_body.get('name'):
        if req_body.get('name').lower() in user_names:
            return "Name already exists", 500 
        else:
            user_data.name = req_body.get('name')
            updated_data['name'] = req_body.get('name')
    else:
        user_data.name = old_data.get('name')
        updated_data['name'] = old_data.get('name')
    
    if req_body.get('age'):
        user_data.age = req_body.get('age')
        updated_data['age'] = req_body.get('age')
    else:
        user_data.age = old_data.get('age')
        updated_data['age'] = old_data.get('age')

    if req_body.get('occupation'):
        user_data.occupation = req_body.get('occupation')
        updated_data['occupation'] = req_body.get('occupation')
    else:
        user_data.occupation = old_data.get('occupation')
        updated_data['occupation'] = old_data.get('occupation')

    db.session.commit()
    

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
def delete_user(user_data,id):

    Interest.query.filter_by(user_id=id).delete()
    User.query.filter_by(id=id).delete()
    db.session.commit()
    data = {
            "message" : "Existing User Deleted",
            "data" : user_data
    }
    return data, 200


def check_complete_body(jsonData):
    if not jsonData.get('name') or not jsonData.get('age') or not jsonData.get('occupation'):
        return False
    return True
