import requests
import json

url = 'http://0.0.0.0:8080/couriers'

data = []
val = dict()
val["courier_id"] = 2
val["courier_type"] = "foot"
val['regions'] = [1, 12, 22]
val["working_hours"] = ["11:35-14:05", "09:00-11:00"]

data.append(val)

val = dict()
val["courier_id"] = 3
val["courier_type"] = "foot"
val['regions'] = []
val["working_hours"] = ["11:35-10:05", "09:00-11:00"]

data.append(val)

r = requests.post(url, json.dumps({'data': data}))
print(r.text)
