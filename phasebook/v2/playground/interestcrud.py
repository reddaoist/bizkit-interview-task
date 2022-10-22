from flask import Blueprint, request, jsonify
from ...models import Interest,db
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
    msg = "Match found" if is_match(getFavNums(id),getFavNums(match_id)) else "No match"
    end = time.time()
    return {"message": msg, "elapsedTime": end - start}, 200

def is_match(fave_numbers_1, fave_numbers_2):
    return set(fave_numbers_2).issubset(set(fave_numbers_1))


# to be implemented
def getFavNums(id):
    return "", 200

def addFavNums(id, req):
    return "", 200

def does_not_exist(id):
    return True
