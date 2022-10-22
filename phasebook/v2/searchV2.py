from flask import Blueprint, request, jsonify
from ..models import User

bp = Blueprint("searchV2", __name__, url_prefix="/v2/search")


@bp.route("")
def search():
    return search_users(request.args.to_dict())


def search_users(args):
    """Search users database

    Parameters:
        args: a dictionary containing the following search parameters:
            id: string
            name: string
            age: string
            occupation: string
  
    Returns:
        a list of users that match the search parameters
    """

    # Implement search here!

    result = []
   
    id_matches = []
    name_matches = []
    age_matches = []
    occupation_matches = []

    users = jsonify(User.query.all())

    if not args:
        return users
    
    for user in users.json:
        
        if int(args.get('id') or 0) == user.get('id'):
            id_matches.append(user)
            continue
        
        if str(args.get('name')).casefold() in str(user.get('name')).casefold():
            name_matches.append(user)
            continue
        
        if user.get('age') in range(int(args.get('age') or 0) -1, int(args.get('age') or 0) +2):
            age_matches.append(user)
            continue
        
        if str(args.get('occupation')).casefold() in str(user.get('occupation')).casefold():
            occupation_matches.append(user)
            continue

    result = id_matches + name_matches + age_matches + occupation_matches
    
    return result


    