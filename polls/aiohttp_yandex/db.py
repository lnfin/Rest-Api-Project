from settings import config_db
import psycopg2
import datetime

conf = config_db['postgres']


def time_check(hours):
    for hour in hours:
        try:
            h1 = int(hour[:2])
            m1 = int(hour[3:5])
            h2 = int(hour[6:8])
            m2 = int(hour[9:11])

            if 0 <= h1 <= 23 and 0 <= h2 <= 23 and 0 <= m1 <= 59 and 0 <= m2 <= 59:
                if h1 * 60 + m1 < h2 * 60 + m2:
                    return True
        except ValueError:
            return False
    return False


def weight_check(weight):
    if 0.01 <= weight <= 50:
        return True
    else:
        return False


def load_capacity(courier_type):
    d = {'foot': 10, 'bike': 15, 'car': 50}
    return d[courier_type]


def time_convert(t):
    return (int(t[:2]) * 60 + int(t[3:5]), int(t[6:8]) * 60 + int(t[9:11]))


def factor(courier_type):
    d = {'foot': 2, 'bike': 5, 'car': 9}
    return d[courier_type]


def string_to_time(dt_str):
    dt, _, us = dt_str.partition(".")
    dt = datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%S")
    us = int(us.rstrip("Z"), 10)
    return dt + datetime.timedelta(microseconds=us)


class DB:
    def __init__(self):
        self.conn = psycopg2.connect(host=conf['host'],
                                     user=conf['user'],
                                     password=conf['password'],
                                     dbname=conf['database'])

    def add_courier(self, couriers):
        cur = self.conn.cursor()
        fields = ['courier_id', 'courier_type', 'regions', 'working_hours']
        errors = []
        success = []
        for courier in couriers:
            if fields == list(courier.keys()) \
                    and [] not in courier.values() \
                    and time_check(courier['working_hours']):
                sql = f'''INSERT into couriers VALUES (\
                        {courier['courier_id']},\
                        '{courier['courier_type']}',\
                        '{str(set(courier['regions']))}',\
                        '{str(set(courier['working_hours'])).replace("'", '"')}');'''
                cur.execute(sql)
                success.append({'id': courier['courier_id']})
            else:
                errors.append({'id': courier['courier_id']})

        if errors:
            return False, errors
        else:
            self.conn.commit()
            return True, success

    def patch_courier(self, id, params):
        cur = self.conn.cursor()
        fields = {"courier_type", "regions", "working_hours"}
        if not set(params.keys()).issubset(fields):
            print(set(params.keys()))
            return False, {}

        for param in params.keys():
            sql = f'''UPDATE couriers SET {param} = '{str(set(params[param]))}' WHERE id = {id};'''
            cur.execute(sql)
        self.conn.commit()

        sql = f'''SELECT * FROM couriers WHERE id = {id};'''
        cur.execute(sql)
        resp = cur.fetchall()
        if not resp:
            return False, {}
        resp = resp[0]
        info = dict()
        info['courier_id'] = resp[0]
        info['courier_type'] = resp[1]
        info['regions'] = resp[2]
        info['working_hours'] = resp[3]
        return True, info

    def add_orders(self, orders):
        cur = self.conn.cursor()
        fields = ["order_id", "weight", "region", "delivery_hours"]
        errors = []
        success = []
        for order in orders:
            if fields == list(order.keys()) and [] not in order.values() and \
                    time_check(order['delivery_hours']) and \
                    weight_check(order['weight']):
                sql = f'''INSERT into orders VALUES (\
                        {order['order_id']},\
                        {order['weight']},\
                       '{order['region']}',\
                       '{str(set(order['delivery_hours'])).replace("'", '"')}');'''
                cur.execute(sql)
                success.append({'id': order['order_id']})
            else:
                errors.append({'id': order['order_id']})

        if errors:
            return False, errors
        else:
            self.conn.commit()
            return True, success

    def assign_orders(self, id):
        cur = self.conn.cursor()
        sql = f'''SELECT * FROM couriers WHERE id = {id};'''
        cur.execute(sql)
        res = cur.fetchall()
        if not res:
            return False, [], ""
        res = res[0]
        courier_type = load_capacity(res[1])
        working_time = [time_convert(t) for t in res[-1]]
        sql = f'''SELECT * FROM orders WHERE region = ANY('{str(set(res[2])).replace("'", '"')}')\
                  AND (weight BETWEEN 0 AND {courier_type});'''
        cur.execute(sql)
        res = cur.fetchall()
        print(res)
        success = []
        for r in res:
            for time in r[-1]:
                time = time_convert(time)
                for work in working_time:
                    if work[0] < time[1] and work[1] > time[0]:
                        sql = f'''SELECT * FROM assigns WHERE order_id = {r[0]};'''
                        cur.execute(sql)
                        in_assigns = cur.fetchall()
                        if not in_assigns:
                            success.append(r)
                        break

        current_time = datetime.datetime.now().isoformat() + "Z"
        ids = []
        for el in success:
            sql = f'''INSERT INTO assigns VALUES({id},{el[0]},'{current_time}','{"0"}');'''
            cur.execute(sql)
            qs = [list(q.values())[0] for q in ids]
            if el[0] not in qs:
                ids.append({"id": el[0]})

        self.conn.commit()
        return True, ids, current_time

    def complete_order(self, req):
        cur = self.conn.cursor()

        sql = f'''SELECT * FROM assigns WHERE order_id = {req['order_id']} AND courier_id = {req['courier_id']};'''
        cur.execute(sql)
        resp = cur.fetchall()
        if not resp:
            return False, ""

        sql = f'''UPDATE assigns SET complete_time = '{req['complete_time']}'  WHERE order_id = {req['order_id']} \
                  AND courier_id = {req['courier_id']};'''
        cur.execute(sql)
        self.conn.commit()
        return True, req['order_id']

    def courier_info(self, courier_id):
        cur = self.conn.cursor()
        sql = f'''SELECT * FROM couriers WHERE id = {courier_id};'''
        cur.execute(sql)
        courier = cur.fetchall()
        if not courier:
            return False, {}

        sql = f'''SELECT * FROM assigns WHERE courier_id = {courier_id} \
                  AND complete_time != '0';'''

        cur.execute(sql)
        resp = cur.fetchall()

        info = dict()
        if not resp:
            info['courier_id'] = courier_id
            info['courier_type'] = courier[0][1]
            info['regions'] = courier[0][2]
            info['working_hours'] = courier[0][3]
            return True, info
        earnings = 500 * factor(courier[0][1]) * len(resp)

        duration = dict()
        for q in resp:
            start = string_to_time(q[2])
            end = string_to_time(q[3])
            duration[q[1]] = (end - start).total_seconds()

        ids = [q[1] for q in resp]

        sql = f'''SELECT id, region FROM orders WHERE id = ANY('{str(set(ids)).replace("'", '"')}');'''
        cur.execute(sql)
        resp = cur.fetchall()
        regions = dict()
        for q in resp:
            if q[1] not in regions.keys():
                regions[q[1]] = []
            regions[q[1]].append(duration[q[0]])

        td = []
        for reg in regions.keys():
            td.append(sum(regions[reg]) / len(regions[reg]))

        t = min(td)

        rating = (60 * 60 - min(abs(t), 60 * 60)) / (60 * 60) * 5

        info['courier_id'] = courier_id
        info['courier_type'] = courier[0][1]
        info['regions'] = courier[0][2]
        info['working_hours'] = courier[0][3]
        info['rating'] = rating
        info['earnings'] = earnings

        return True, info
