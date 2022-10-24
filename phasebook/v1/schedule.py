from flask import Blueprint, request
from .data.schedule_data import SCHEDULES
from datetime import datetime


bp = Blueprint("schedule", __name__, url_prefix="/schedule")

# online tech interview requirements
# https://verbena-calculator-b7c.notion.site/BizKit-Technical-Interview-Problem-5de9f9d9347d42a8bdc14e540c15002b

@bp.route("<int:user_id>", methods=['POST'])
def schedule(user_id):
    ids = [int(e.get('user_id')) for e in SCHEDULES]

    

    if user_id not in ids:

        schedules = []
        schedule = request.json['start'] + " - " + request.json['end']
        schedules.append(schedule) 

        data = {
            "user_id" : str(user_id),
            "schedules" : schedules
        }

        SCHEDULES.append(data)
        return data, 200
    else:

        index = ids.index(user_id)

        schedules = SCHEDULES[index].get('schedules')
        schedule = request.json['start'] + " - " + request.json['end']

        if schedule not in schedules:
            schedules.append(schedule)

        schedules = sorted(schedules) 
        schedules = fuse(schedules)   

        data = {
            "user_id" : str(user_id),
            "schedules" : schedules
        }

        SCHEDULES[index] = data
            
        return data, 200

def fuse(schedules):


    # list of tuples
    ranges = [(sched[0:5], sched[8:13]) for sched in schedules]

    
    # reference implementation in stackoverflow
    # https://stackoverflow.com/questions/34797525/how-to-correctly-merge-overlapping-datetime-ranges-in-python
    
    #------------------------------------------------------------
    result = []
    t_old = ranges[0]
    for t in ranges[1:]:
        print("for")
        if t_old[1] >= t[0]:
            t_old = ((min(t_old[0], t[0]), max(t_old[1], t[1])))
        else:
            result.append(t_old)
            t_old = t
    else:
        print("else")
        result.append(t_old)
    #------------------------------------------------------------

    fused = []
    for r in result:
        sched = r[0] + " - " + r[1]
        fused.append(sched)

    return fused

         