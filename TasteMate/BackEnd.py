import string
import random
from datetime import datetime
import json
import haversine as hs
import geocoder
from TasteMate import db
from TasteMate.Models import *


def add_review(user_id, business_id, stars, text, date):
    rev_id = ''.join(random.choices(string.ascii_uppercase +string.digits, k=20))

    while(Reviews.query.filter_by(review_id = rev_id).first()):
        rev_id = ''.join(random.choices(string.ascii_uppercase +string.digits, k=20))

    new_review = Reviews(review_id = rev_id,user_id=user_id, business_id= business_id, stars=stars, text=text, date=date)        
    db.session.add(new_review)
    bus = Business.query.filter_by(business_id = business_id).first()
    bus.stars = round((float(bus.stars)*(bus.review_count) + int(stars))/(bus.review_count + 1),2)
    bus.review_count += 1
    db.session.commit()

def delete_review(review_id):
    rev = Reviews.query.filter_by(review_id = review_id).first()
    bus = Business.query.filter_by(business_id = rev.business_id).first()
    bus.stars = 0 if bus.review_count == 1 else (float(bus.stars)*(bus.review_count) - rev.stars)/(bus.review_count - 1)
    bus.stars = round(bus.stars,2)
    bus.review_count -= 1
    db.session.delete(rev)
    db.session.commit()

def openclose(business_id):
    days = {0:'Monday',1:'Tuesday',2:'Wednesday',3:'Thursday',4:'Friday',5:'Saturday',6:'Sunday'}
    bus = Business.query.filter_by(business_id = business_id).first()
    now = int((''.join(datetime.now().strftime("%d/%m/%Y %H:%M:%S").split(" ")[1].strip().split(":")))[:-2])
    if bus.hours is None or len(bus.hours) < 5:
        return "Data Not Available"
    today = days[datetime.now().weekday()]
    try:
        timing = json.loads(bus.hours.replace("'","\""))
    except:
        print('here')
        print(bus.hours.replace("'","\""))
        print('here')
        return "Data Not Available"
    if today not in timing:
        return "Closed"
    opt = int(''.join(timing[today].split("-")[0].strip().split(":")))
    clt = opt = int(''.join(timing[today].split("-")[1].strip().split(":")))
    if now < opt or now > clt:
        return "Closed"
    else:
        return "Open"
    
def get_dist(curlat,curlon,buslat,buslon):
    return hs.haversine(tuple([curlat,curlon]),tuple([buslat,buslon]))


def search_buss(name=None,catlist=[], showopen = False , dist = 20,filterdist = False):
    results = Business.query
    if name:
        results = results.filter(Business.name.ilike(f"%{name}%"))
    if len(catlist):
        for cat in catlist:
            results = results.filter(Business.categories.ilike(f"%{cat}%"))
    results = results.all()
    if filterdist:
        g = geocoder.ip('me')
        g = list(g.latlng)
        results = [r for r in results if get_dist(g[0],g[1],r.latitude,r.longitude) <= float(dist)]
    if showopen:
        results = [r for r in results if openclose(r.business_id) == "Open"]
    
    results = sorted(results, key=lambda x: x.review_count, reverse=True)
    return results



'''
validate func inp = user_id pass out true false in app.py
add user inp = user_d username pass add to users table
get bus res input dict based on cat.pkl out buss list
open/close based on cur time and day inp check box and cur time date
distance input lat log range
business name input business name
user reviews input user_id
busines reviews input business_id
'''