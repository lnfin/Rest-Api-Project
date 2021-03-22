import requests
import time
import json

url = 'http://0.0.0.0:8080/couriers'

curr = time.time()

data = []
for i in range(1, 8000):
    val = dict()
    val["courier_id"] = i
    val["courier_type"] = "foot"
    val['regions'] = [1, 12, 22]
    val["working_hours"] = ["11:35-14:05", "09:00-11:00"]

    data.append(val)
    print(i)

print(data[-1])
r = requests.post(url, json.dumps({'data': data}))

f = time.time()
print('Start time:', curr)
print('End time:', f)
print("All:", int(f - curr))
