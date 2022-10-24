from flask import Blueprint, request

from .data.search_data import USERS


bp = Blueprint("search", __name__, url_prefix="/search")


@bp.route("")
def search():
    return search_users(request.args.to_dict()), 200


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

    # Search Specifications

    # All of the search parameters are optional. That means a user can 
    #   pass no search parameter and the function should return all users.
    #   The user can also pass just the id as a parameter and it should
    #   just return the user with that id. The user can also pass multiple 
    #   parameters and the function should return all the users that match 
    #   ANY of the parameters provided.
    # The id is unique. If the id is included in the search parameters,
    #   then immediately include the user with the passed id.
    # The name can be partially matched and is case insensitive. 
    #   That means that if we have users with names John Doe, Jane Doe,
    #   and Joe Doe, passing the word "doe" to the name parameter should 
    #   include all of them in the results.
    # The age parameter should include users that are in the range of 
    #   age - 1 to age + 1. This means that if we pass 26 to the age parameter,
    #   we should include users with ages 25 to 27.
    # The occupation parameter can be partially matched and is case insensitive.
    #   This means that if we pass "er" to the occupation parameter,
    #   we should include all users with an occupation that contains "er"
    #   in the results.
    # Do not include a user in the results more than once.

    result = []
   
    id_matches = []
    name_matches = []
    age_matches = []
    occupation_matches = []

    if not args:
        return USERS

    for user in USERS:
        
        if args.get('id') == user.get('id'):
            id_matches.append(user)
            continue
        
        if str(args.get('name')).casefold() in str(user.get('name')).casefold():
            name_matches.append(user)
            continue
        
        if int(user.get('age') or 0) in range(int(args.get('age') or 0) -1, int(args.get('age') or 0) +2):
            age_matches.append(user)
            continue
        
        if str(args.get('occupation')).casefold() in str(user.get('occupation')).casefold():
            occupation_matches.append(user)
            continue

    result = id_matches + name_matches + age_matches + occupation_matches
    
    return result


    
    
