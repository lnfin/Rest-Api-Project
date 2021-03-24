from settings import config_db
import psycopg2

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
        resp = cur.fetchall()[0]
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
        return
