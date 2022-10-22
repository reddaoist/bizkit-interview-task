from flask import Blueprint, request, jsonify
from ...models import User,Interest,db
import time


bp = Blueprint("interestsv2", __name__, url_prefix="/v2/interests")

@bp.route("<int:id>",methods=['GET', 'POST'])
def favnum(id = None):

    if not id:
        return "Invalid id", 404
    elif does_not_exist(id):
        return "Invalid id", 404
    else:
        if request.method == 'GET':
            return getFavNums(id)
        else:
            return addFavNums(id, request.json)


@bp.route("<int:id>/match/<int:match_id>",methods=['GET'])
def match(id = None, match_id = None):
    if not id or not match_id:
        return "Invalid id/s", 404
    elif does_not_exist(id) or does_not_exist(match_id):
        return "Invalid id/s", 404
    
    start = time.time()

    user_nums = [interest['fav_num'] for interest in getFavNums(id).json]
    other_user_nums = [interest['fav_num'] for interest in getFavNums(match_id).json]
    
    msg = "Match found" if is_match(user_nums, other_user_nums) else "No match"
    
    end = time.time()

    data = {
        "message" : msg,
        "elapsedTime" : end - start,
        "fav_nums" : {
            "user" : user_nums,
            "other" : other_user_nums
        }
    }
    
    return data, 200



def is_match(fave_numbers_1, fave_numbers_2):
    return set(fave_numbers_2).issubset(set(fave_numbers_1))

def getFavNums(id):
    resp = jsonify(Interest.query.filter_by(user_id=id).all())
    return resp

def addFavNums(id, req):

    new_fave_nums = [num for num in req.get('favnums')]
    curr_fave_nums = [interest['fav_num'] for interest in getFavNums(id).json]
    
    count = 0
    added = []

    for num in new_fave_nums:
        if num not in curr_fave_nums:
            new_num = Interest(user_id=id, fav_num=num)
            db.session.add(new_num)
            added.append(new_num)
            count = count + 1
    
    db.session.commit()
    msg = str(count) + ' Favorite Numbers Added'
    data = {
        'message' : msg,
        'data'  : added
    }
    return data, 200

def does_not_exist(id):
    return not bool(User.query.filter_by(id=id).first())
   
